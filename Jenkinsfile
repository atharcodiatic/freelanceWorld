pipeline {
    agent { dockerfile true }
stages {
        stage('build') {
            steps {
                echo "clone successfull"
            
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
