pipeline {

  environment {
    PROJECT = "rising-minutia-254502"
    APP_NAME = "pubsub_bq_kubernetes"
    CLUSTER = "jenkins-cd"
    CLUSTER_ZONE = "us-east1-d"
    IMAGE_TAG = "gcr.io/${PROJECT}/${APP_NAME}:v${env.BUILD_NUMBER}"
    JENKINS_CRED = "rising-minutia-254502"
  }

  agent {
    kubernetes {
      label 'pubsub_bq_kubernetes-app'
      defaultContainer 'jnlp'
      yaml """
apiVersion: v1
kind: Pod
metadata:
labels:
  component: ci
spec:
  # Use service account that can deploy to all namespaces
  serviceAccountName: cd-jenkins
  containers:
  - name: golang
    image: golang:1.10
    command:
    - cat
    tty: true
  - name: pythonenv
    image: gcr.io/rising-minutia-254502/python-image
    command:
    - cat
    tty: true
  - name: gcloud
    image: gcr.io/cloud-builders/gcloud
    command:
    - cat
    tty: true
  - name: kubectl
    image: gcr.io/cloud-builders/kubectl
    command:
    - cat
    tty: true
"""
}
  }
  stages {
    stage('Test') {
      steps {
        container('pythonenv') {
          sh label: '', script: "nosetests --with-xunit --all-modules --traverse-namespace --with-coverage --cover-package=pubsub-pipe-image --cover-inclusive"
          sh label: '', script: "python -m coverage xml --include=pubsub-pipe-image*"
          sh label: '', script: "pylint -f parseable -d I0011,R0801 pubsub-pipe-image | tee pylint.out"
        }
      }
    }
    stage('Build and push image with Container Builder') {
      steps {
        container('gcloud') {
          sh "PYTHONUNBUFFERED=1 gcloud builds submit -t ${IMAGE_TAG} ./pubsub-pipe-image"
        }
      }
    }
    stage('Deploy Production') {
      // Production branch
      // when { branch 'master' }
      steps{
        container('kubectl') {
          sh label: '', script: 'echo "IMAGE_TAG is : ${IMAGE_TAG}"'
          // Change deployed image in production to the one we just built
          sh("sed -i.bak 's#gcr.io/rising-minutia-254502/pubsub-bq-pipe:v1#${IMAGE_TAG}#' *.yaml")
          // sh label: '', script: 'kubectl create ns production'
          step([$class: 'KubernetesEngineBuilder',namespace:'production', projectId: env.PROJECT, clusterName: env.CLUSTER, zone: env.CLUSTER_ZONE, manifestPattern: 'twitter-stream.yaml', credentialsId: env.JENKINS_CRED, verifyDeployments: true])
          step([$class: 'KubernetesEngineBuilder',namespace:'production', projectId: env.PROJECT, clusterName: env.CLUSTER, zone: env.CLUSTER_ZONE, manifestPattern: 'bigquery-controller.yaml', credentialsId: env.JENKINS_CRED, verifyDeployments: true])
        }
      }
    }
    stage('Publish Reports'){
      steps{
        container('pythonenv'){
          cobertura autoUpdateHealth: false, autoUpdateStability: false, coberturaReportFile: 'coverage.xml', conditionalCoverageTargets: '70, 0, 0', failUnhealthy: false, failUnstable: false, lineCoverageTargets: '80, 0, 0', maxNumberOfBuilds: 0, methodCoverageTargets: '80, 0, 0', onlyStable: false, sourceEncoding: 'ASCII', zoomCoverageChart: false
          //junit 'nosetests.xml'
          warnings canComputeNew: false, canResolveRelativePaths: false, categoriesPattern: '', defaultEncoding: '', excludePattern: '', healthy: '', includePattern: '', messagesPattern: '', parserConfigurations: [[parserName: 'PyLint', pattern: 'pylint.out']], unHealthy: ''
        }
      }
    }
  }
}
