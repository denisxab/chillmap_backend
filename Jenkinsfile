pipeline {

    agent { 
		docker { 
            dockerfile: "Dockerfile_Jenkins"
		} 
	}

    stages {
        stage('Lint Python'){
            stages{
                sh 'flake8 .'
            }
        }

        stage('Test Django'){
            steps{
                sh "invoke prod.testDjango --echo"
            }
        }
    }

}
