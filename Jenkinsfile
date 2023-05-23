pipeline {

    agent { 
        dockerfile "Dockerfile_Jenkins"
	}

    stages {
        stage('Lint Python'){
            steps {
                sh "flake8 ."
            }
        }

        stage('Test Django'){
            steps {
                sh "invoke prod.testDjango --echo"
            }
        }
    }

}
