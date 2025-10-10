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
            echo "OMG SUCCESS: Build ${env.BUILD_NUMBER} completed successfully!"
        }
        failure {
            echo "Shit FAILURE: Build ${env.BUILD_NUMBER} failed. Check console logs."
        }
    }
}


// pipeline {
//   agent any

//   environment {
//     IMAGE = "mrvandana1/scientific_calculator"
//     // option: pick tag from git commit or build number
//     IMAGE_TAG = "${env.BUILD_NUMBER}"
//     FULL_IMAGE = "${env.IMAGE}:${env.IMAGE_TAG}"
//   }

//   stages {
//     stage('Checkout') {
//       steps {
//         checkout scm
//       }
//     }

//     stage('Install deps & Test') {
//       steps {
//         sh 'python3 -m pip install --upgrade pip'
//         sh 'pip3 install -r requirements.txt'
//         sh 'pytest -q'
//       }
//     }

//     stage('Build Docker Image') {
//       steps {
//         sh "docker build -t ${FULL_IMAGE} ."
//       }
//     }

//     stage('Docker Login & Push') {
//       steps {
//         withCredentials([usernamePassword(credentialsId: 'mrvandana1', usernameVariable: 'mrvandana1', passwordVariable: 'W)%Jx59;/KA:s&L')]) {
//           sh 'echo $DOCKERHUB_PASS | docker login -u $DOCKERHUB_USER --password-stdin'
//           sh "docker push ${FULL_IMAGE}"
//         }
//       }
//     }

//     stage('Deploy (Ansible)') {
//       steps {
//         // Ensure ansible & community.docker present on Jenkins agent
//         sh "ansible-galaxy collection install community.docker || true"
//         sh "ansible-playbook -i ansible/inventory.ini ansible/deploy.yml --extra-vars \"image=${FULL_IMAGE}\""
//       }
//     }
//   }

// //   post {
// //     success {
// //       mail to: 'team@example.com',
// //            subject: "SUCCESS: Build ${env.JOB_NAME} #${env.BUILD_NUMBER}",
// //            body: "Build successful. Image: ${FULL_IMAGE}"
// //     }
// //     failure {
// //       mail to: 'team@example.com',
// //            subject: "FAILURE: Build ${env.JOB_NAME} #${env.BUILD_NUMBER}",
// //            body: "Build failed. Check console output."
// //     }
// //   }
// }
