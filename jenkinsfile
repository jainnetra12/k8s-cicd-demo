// Jenkinsfile
pipeline {
    // This uses a shell agent, assuming you fix the 'docker: not found' issue on the main node
    agent any 

    // Define environment variables for substitution
    environment {
        DOCKER_USER = 'jainnetra123' 
        IMAGE_REPO = 'student-dashboard'
        CREDENTIAL_ID = 'dockerhub-credentials'
    }

    stages {
        stage('Checkout Code') {
            steps {
                echo "Checking out ${BRANCH_NAME} branch..."
            }
        }
        
        stage('Build & Push Docker Image') {
            steps {
                script {
                    def tag = "${env.BRANCH_NAME}-${env.BUILD_NUMBER}"
                    def image = "${DOCKER_USER}/${IMAGE_REPO}:${tag}"
                    
                    // 1. Build the image
                    sh "docker build -t ${image} ."
                    
                    // 2. Login to DockerHub using stored credentials
                    withCredentials([usernamePassword(credentialsId: "${CREDENTIAL_ID}", usernameVariable: 'DOCKER_USER_VAR', passwordVariable: 'DOCKER_PASS_VAR')]) {
                        sh "echo ${DOCKER_PASS_VAR} | docker login -u ${DOCKER_USER_VAR} --password-stdin"
                        // 3. Push the image
                        sh "docker push ${image}"
                        sh "docker logout"
                    }
                    
                    env.IMAGE_NAME = image
                }
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                script {
                    def envName = (env.BRANCH_NAME == 'main') ? "production" : "test"
                    
                    // The image name must be explicitly set here for kubectl to use it
                    sh """
                        # We use 'sed' to substitute the dynamic image tag and env name into the YAML file
                        sed -i 's|YOUR_DOCKERHUB_USERNAME/student-dashboard:TAG_NAME|${env.IMAGE_NAME}|g' deployment.yaml
                        sed -i 's|ENV_NAME_PLACEHOLDER|${envName}|g' deployment.yaml
                        
                        # Apply the deployment to Kubernetes
                        kubectl apply -f deployment.yaml
                    """
                    echo "Deployment complete for ${envName} using image ${env.IMAGE_NAME}"
                }
            }
        }
    }
}