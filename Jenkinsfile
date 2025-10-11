pipeline {
    agent any

    environment {
        IMAGE = "mrvandana1/scientific_calculator"
        TAG = "${env.BUILD_NUMBER}"
        FULL_IMAGE = "${IMAGE}:${TAG}"
        PATH = "/usr/local/bin:${env.PATH}" 
    }

    stages {
        stage('Checkout') {
            steps {
                echo "...Checking out source code..."
                checkout scm
            }
        }

        stage('Install dependencies & Run Tests') {
            steps {
                echo "Installing dependencies and running tests..."
                sh '''
                    python3 -m venv venv
                    . venv/bin/activate
                    pip install --upgrade pip
                    pip install -r requirements.txt
                    pytest -q
                '''
            }
        }

        stage('Build Docker Image') {
            steps {
                echo "bros  Building Docker image..."
                sh "docker build -t ${FULL_IMAGE} ."
            }
        }

        stage('Push to DockerHub') {
            steps {
                echo " Logging into DockerHub and pushing image..."
                withCredentials([usernamePassword(credentialsId: 'mrvandana1', usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]) {
                    sh '''
                        echo "$DOCKER_PASS" | docker login -u "$DOCKER_USER" --password-stdin
                        docker push ${FULL_IMAGE}
                    '''
                }
            }
        }

        stage('Deploy via Ansible') {
            steps {
                echo "Daymn Deploying using Ansible..."
                sh '''
                    ansible-galaxy collection install community.docker || true
                    ansible-playbook -i ansible/inventory.ini ansible/deploy.yml --extra-vars "image=${FULL_IMAGE}"
                '''
            }
        }

        stage('Cleanup Docker Space') {
            steps {
                echo "ahh Cleaning up unused Docker data..."
                sh 'docker system prune -af || true'
            }
        }
    }


    post {
        success {
            echo "SUCCESS: Build ${env.BUILD_NUMBER} completed successfully!"
            mail to: 'vandanamohanaraj@gmail.com',
                 subject: "SUCCESS: ${env.JOB_NAME} #${env.BUILD_NUMBER}",
                 body: """Hey Mohan,

                    My Jenkins build completed successfully Damyn

                    Details:
                    - Job: ${env.JOB_NAME}
                    - Build number: ${env.BUILD_NUMBER}
                    - Image: ${env.FULL_IMAGE}

                    You can check the full logs here:
                    ${env.BUILD_URL}
                    """
                            }
                            failure {
                                echo "FAILURE: Build ${env.BUILD_NUMBER} failed. Check console logs."
                                mail to: 'vandanamohanaraj@gmail.com',
                                    subject: "FAILURE: ${env.JOB_NAME} #${env.BUILD_NUMBER}",
                                    body: """Hey Mohan,you failed here bro Your Jenkins build *failed* 

                                        Details:
                                        - Job: ${env.JOB_NAME}
                                        - Build number: ${env.BUILD_NUMBER}

                                        Check console output here:
                                        ${env.BUILD_URL}
                                        """
        }
    }
}
