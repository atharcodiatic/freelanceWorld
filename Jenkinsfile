pipeline {
    agent { Dockerfile true }
stages {
        stage('build') {
            
            steps {
                retry(3){
                echo "clone successfull"
                sh "sudo docker compose up --build" } 
            }
            timeout(time:20, unit: "SECONDS")
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
