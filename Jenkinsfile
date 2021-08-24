pipeline {
    agent any
    stages {
        stage('Build the Artifacts') {
            steps {
                sh """
                    mkdir elk_confs && \
                    mkdir elk_confs/test && \
                    mkdir elk_confs/test/configmap && \
                    mkdir elk_confs/test/secrets && \
                    mkdir elk_confs/acc && \
                    mkdir elk_confs/acc/configmap && \
                    mkdir elk_confs/acc/secrets && \
                    mkdir elk_confs/reports 
                """

                // Generate the artifacts
                sh '$CASC_JENKINS_CONFIG/../tools/kustomize build environments/test/configmap -o elk_confs/test/configmap'
                sh '$CASC_JENKINS_CONFIG/../tools/kustomize build environments/test/secret -o elk_confs/test/secrets'

                sh '$CASC_JENKINS_CONFIG/../tools/kustomize build environments/acc/configmap -o elk_confs/acc/configmap'
                sh '$CASC_JENKINS_CONFIG/../tools/kustomize build environments/acc/secret -o elk_confs/acc/secrets'
            }
        }

        stage('Deploy to Test Environment') {
            steps {
                input(id: 'userInput', message: 'Deploy to test environment?')
                sh 'kubectl apply --kubeconfig=$CASC_JENKINS_CONFIG/../conf/test-kube.config \
                  -f elk_confs/test/configmap'
                
                sh 'kubectl apply --kubeconfig=$CASC_JENKINS_CONFIG/../conf/test-kube.config \
                  -f elk_confs/test/secrets'
            }
        }

        stage('Deploy to Primary Environment') {
            steps {
                input(id: 'userInput', message: 'Deploy to primary environment?')
                sh 'kubectl apply --kubeconfig=$CASC_JENKINS_CONFIG/../conf/acc-kube.config \
                  -f elk_confs/acc/configmap'
                
                sh 'kubectl apply --kubeconfig=$CASC_JENKINS_CONFIG/../conf/acc-kube.config \
                  -f elk_confs/acc/secrets'
            }
        }

        stage('Post Deployment Checks') {
            steps {
                sh 'echo "Waiting for Kubernetes to spin the pods" && sleep 40'

                // test-elastic-system is the name of the test namespace
                // Check if the replication is correct
                sh 'python3 tests/check_deployment_replication_status.py elastic-system \
                $CASC_JENKINS_CONFIG/../conf/acc-kube.config >> elk_confs/reports/acc_deployment_checks_result.txt'

                // Build the app inspector image
                sh 'docker build -t docker.io/reggievaldez/app-function-inspector tests/jobs/app_function_inspector/.'

                // Deploy the inspector job
                sh 'kubectl apply --kubeconfig=$CASC_JENKINS_CONFIG/../conf/acc-kube.config \
                  -f tests/jobs/inspector-job.yml && sleep 8'

                // Check if the job succeeded
                sh 'kubectl get job app-function-inspector -o jsonpath={.status.succeeded} \
                --kubeconfig=$CASC_JENKINS_CONFIG/../conf/acc-kube.config'

                sh 'zip -r artifact.zip elk_confs'
                archiveArtifacts artifacts: 'artifact.zip'
            }
        }
    }

    post { 
        always { 
            echo 'Cleaning workbench...!'
            sh 'rm -r elk_confs'

            // TODO post run notifications

        }
    }
}