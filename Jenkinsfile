pipeline {
  agent any

  environment {
    IMAGE = "mrvandana1/scientific-calculator"
    // option: pick tag from git commit or build number
    IMAGE_TAG = "${env.BUILD_NUMBER}"
    FULL_IMAGE = "${env.IMAGE}:${env.IMAGE_TAG}"
  }

  stages {
    stage('Checkout') {
      steps {
        checkout scm
      }
    }

    stage('Install deps & Test') {
      steps {
        sh 'python3 -m pip install --upgrade pip'
        sh 'pip3 install -r requirements.txt'
        sh 'pytest -q'
      }
    }

    stage('Build Docker Image') {
      steps {
        sh "docker build -t ${FULL_IMAGE} ."
      }
    }

    stage('Docker Login & Push') {
      steps {
        withCredentials([usernamePassword(credentialsId: 'mrvandana1', usernameVariable: 'mrvandana1', passwordVariable: 'W)%Jx59;/KA:s&L')]) {
          sh 'echo $DOCKERHUB_PASS | docker login -u $DOCKERHUB_USER --password-stdin'
          sh "docker push ${FULL_IMAGE}"
        }
      }
    }

    stage('Deploy (Ansible)') {
      steps {
        // Ensure ansible & community.docker present on Jenkins agent
        sh "ansible-galaxy collection install community.docker || true"
        sh "ansible-playbook -i ansible/inventory.ini ansible/deploy.yml --extra-vars \"image=${FULL_IMAGE}\""
      }
    }
  }

//   post {
//     success {
//       mail to: 'team@example.com',
//            subject: "SUCCESS: Build ${env.JOB_NAME} #${env.BUILD_NUMBER}",
//            body: "Build successful. Image: ${FULL_IMAGE}"
//     }
//     failure {
//       mail to: 'team@example.com',
//            subject: "FAILURE: Build ${env.JOB_NAME} #${env.BUILD_NUMBER}",
//            body: "Build failed. Check console output."
//     }
//   }
}
