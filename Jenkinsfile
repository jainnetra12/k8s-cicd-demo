// Jenkinsfile - Simplified for Execution
pipeline {
    agent any // Run on the main node

    stages {
        stage('Build & Push Docker Image') {
            steps {
                script {
                    // Define variables locally within the script block
                    def DOCKER_USER = "jainnetra123"
                    def IMAGE_REPO = "student-dashboard"
                    def CREDENTIAL_ID = "dockerhub-credentials"
                    def tag = "${env.BRANCH_NAME}-${env.BUILD_NUMBER}"
                    def image = "${DOCKER_USER}/${IMAGE_REPO}:${tag}"
                    
                    echo "Starting build for image: ${image}"
                    
                    // 1. Build the image
                    sh "docker build -t ${image} ."
                    
                    // 2. Login to DockerHub using stored credentials
                    withCredentials([usernamePassword(credentialsId: "${CREDENTIAL_ID}", usernameVariable: 'DOCKER_USER_VAR', passwordVariable: 'DOCKER_PASS_VAR')]) {
                        sh "echo ${DOCKER_PASS_VAR} | docker login -u ${DOCKER_USER_VAR} --password-stdin"
                        // 3. Push the image
                        sh "docker push ${image}"
                        sh "docker logout"
                    }
                    
                    env.IMAGE_NAME = image // Set variable for next stage
                }
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                script {
                    def envName = (env.BRANCH_NAME == 'main') ? "production" : "test"
                    
                    sh "echo Deploying ${env.IMAGE_NAME} to ${envName} environment"
                    
                    // Substitute image tag and environment name in the YAML file
                    sh """
                        sed -i 's|YOUR_DOCKERHUB_USERNAME/student-dashboard:TAG_NAME|${env.IMAGE_NAME}|g' deployment.yaml
                        sed -i 's|ENV_NAME_PLACEHOLDER|${envName}|g' deployment.yaml
                        
                        # Apply the deployment to Kubernetes
                        kubectl apply -f deployment.yaml
                    """
                }
            }
        }
    }
}