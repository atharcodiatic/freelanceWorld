pipeline {
    agent {dockerfile true }
stages {
        stage('build') {
            steps {
                echo "clone successfull"
                sh "sudo docker compose up --build"  
            }
        }
        stage('test'){
            steps{
                echo "test started"
            }
        }
        post {
            always {
                echo "executing test "
            }
            
            success{
                echo "finish building"
            }
    }

        }

post {
        always {
            echo "running build"
        }
        success{
            echo "finish building"
        }
        failure {
                echo "failed"
            }
    }
}
