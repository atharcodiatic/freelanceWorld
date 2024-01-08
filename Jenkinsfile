pipeline {
    agent any
stages {
        stage('build') {
            steps {

                echo "clone successfull"
                sh sudo docker compose up --build 
            
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
    }
}
