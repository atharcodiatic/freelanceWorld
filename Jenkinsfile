pipeline {
    agent { dockerfile true }
stages {
        stage('clone') {
            steps {
                echo "clone successfull"
                sh 'node --version'
                sh 'svn --version'
            }
        }
        }

post {
        always {
            junit 'build/reports/**/*.xml'
        }
    }
}
