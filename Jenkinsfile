pipeline {
    agent { Dockerfile true }
stages {
        stage('build') {
            
            steps {
                options {
                timeout(time: 4, unit: 'SECONDS') 
            }
                
                echo "clone successfull"
                sh "sudo docker compose up --build" 
            }
        }
        stage('test'){

            steps{
                echo "test started"
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
