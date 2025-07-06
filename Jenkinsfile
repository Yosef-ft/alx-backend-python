pipeline{
    agent {
        docker { image 'python:3.10-slim' }
    }

    stages{
        stage('Prepare Environment') {
            steps {
                sh 'apt-get update && apt-get install -y git docker-ce-cli'
            }
        }      

        stage("Pulls messaging app"){
            steps{
                git(
                    url: 'https://github.com/Yosef-ft/alx-backend-python.git',
                    // git branch
                    branch: 'main',
                    credentialsId: 'messaging-app-token'
                )
            }
        }
        stage("Install dependencies"){
            steps{
                sh '''
                    python3 -m venv .venv
                    source .venv/bin/activate
                    # "messaging_app/requirements.txt", "pip3 install"
                    pip install -r messaging_app/requirements.txt
                '''
            }
        }
        stage("Run test"){
            steps{
                sh '''
                   source .venv/bin/activate
                   pytest messaging_app/ --junitxml="test-report.xml" 
                '''
            }
        }
        stage("Build and push to docker hub"){
            steps{
                withCredentials([usernamePassword(credentialsId: 'dockerhub-credentials', usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]) {
                    sh '''

                        echo "$DOCKER_PASS" | docker login -u "$DOCKER_USER" --password-stdin

                        IMAGE_NAME="yosefft/messaging-app:latest"

                        docker build -t $IMAGE_NAME .
                        docker push $IMAGE_NAME

                        docker logout
                    '''
                }
            }
        }
    }
    post {
        always {
            node {
                junit 'path/to/results.xml'
            }
        }
    }    
}