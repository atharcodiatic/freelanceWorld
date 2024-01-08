pipeline {
    agent any
    stages {
            stage('build') {
                options {
                    timeout(time: 4, unit: 'SECONDS') 
                            }
                steps {
                    echo "clone successfull"
                    sh " docker compose up --build" 
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
