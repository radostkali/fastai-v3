<template>
  <div class='center'>
    <div class='title'>Entity identification project</div>
    <p>
      A demo UI to illustrate the cropping feature in improving the native application usability. 
    </p>
    <div class='content'>
      <div class='no-display'>
        <input ref='fileInput'
               class='no-display'
               type='file'
               name='file'
               accept='image/*'
               @change='showPicked'>
      </div>
      <button class='choose-file-button' type='button' @click="showPicker">Select Image</button>
      <div class='upload-label'>
        <label>{{ imageName ? imageName : 'No file chosen' }}</label>
      </div>
      <div>
        <img :class="imageUrl && !editImage ? '' : 'no-display'" alt='Chosen Image' height='400' :src="imageUrl">
      </div>
      <cropper
        v-if="editImage"
        classname="cropper"
        :src="imageUrl"
        @change="crop"
      ></cropper>
      <div 
        class='result-label' 
        :style="'color: ' + responseMsgColor">
        <label>{{responseMsg}}</label>
      </div>
      <div class='result-label' v-if="editImage">
        <label></label>
      </div>
      <div class='analyze'>
        <button v-if="!editImage" class='analyze-button' type='button' @click="analyze">{{ analyzeBtnTitle }}</button>
        <button v-if="editImage" class='resubmit-button' type='button' @click="resubmit">{{ resubmitBtnTitle }}</button>
      </div>
    </div>
  </div>
</template>

<script>
import { Cropper } from 'vue-advanced-cropper'

let dataURLtoBlob = require('blueimp-canvas-to-blob')

export default {
  name: 'UploadImage',
  components: { Cropper },
  data () {
    return {
      imageName: null,
      imageUrl: null,
      responseMsg: null,
      responseMsgColor: '',
      analyzeBtnTitle: 'Analyze',
      resubmitBtnTitle: 'Resubmit',
      editImage: false,
    }
  },
  methods: {
    crop({coordinates, canvas}) {
      this.cropedImage = canvas.toDataURL()
      console.log(this.cropedImage, coordinates)
    },
    showPicker () {
      const elem = this.$refs.fileInput
      elem.click()
    },
    showPicked () {
      this.pickedImage = this.$refs.fileInput.files[0]
      this.imageName = this.pickedImage.name
      this.imageUrl = URL.createObjectURL(this.pickedImage)
    },
    resubmit () {
      if (this.editImage) {
        this.resubmitBtnTitle = 'Resubmiting...'
        this.responseMsg = ''
        let blob = dataURLtoBlob(this.cropedImage)
        let fileData = new FormData();
        fileData.append("file", blob);
        let r = new Promise((resolve, reject) => {
            this.axios.post('/analyze', fileData)
              .then(response => {
                if (response.status === 200) {
                  resolve(response.data)
                } else {
                  reject(new Error('Upload image error'))
                }
              })
              .catch(error => {
                console.log(error)
                reject(new Error('Upload image error'))
              })
          })
          r.then(
            (response) => {
              this.imageUrl = this.cropedImage
              this.pickedImage = blob
              if (response.result === true) {
                this.responseMsg = 'The image reveals identity'
                this.responseMsgColor = '#c42424'
                this.editImage = false
              } else {
                this.responseMsg = 'No identity detected'
                this.responseMsgColor = '#5ccb52'
                this.editImage = false
              }
              this.resubmitBtnTitle = 'Resubmit'
            },
            (error) => {
              alert(error)
              this.resubmitBtnTitle = 'Resubmit'
            }
          )
      }
    },
    analyze () {
      if (this.pickedImage) {
        this.analyzeBtnTitle = 'Analyzing...'
        this.responseMsg = ''
        let fileData = new FormData();
        fileData.append("file", this.pickedImage);
        let r = new Promise((resolve, reject) => {
            this.axios.post('/analyze', fileData)
              .then(response => {
                if (response.status === 200) {
                  resolve(response.data)
                } else {
                  reject(new Error('Upload image error'))
                }
              })
              .catch(error => {
                console.log(error)
                reject(new Error('Upload image error'))
              })
          })
          r.then(
            (response) => {
              if (response.result === true) {
                this.editImage = true
                this.responseMsg = 'Crop out the regions that could reveal identity'
                this.responseMsgColor = '#262626'
              } else {
                this.responseMsg = 'No identity detected'
                this.responseMsgColor = '#5ccb52'
                this.editImage = false
              }
              this.analyzeBtnTitle = 'Analyze'
            },
            (error) => {
              alert(error)
              this.analyzeBtnTitle = 'Analyze'
            }
          )
      }
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
body {
    background-color: #fff;
}

.no-display {
    display: none;
}

.center {
    margin: auto;
    padding: 10px 50px;
    text-align: center;
    font-size: 14px;
}

.title {
    font-size: 30px;
    margin-top: 1em;
    margin-bottom: 1em;
    color: #262626;
}

.content {
    margin-top: 5em;
}

.analyze {
    margin-top: 3em;
    margin-bottom: 5em;
}

.upload-label {
    padding: 10px;
    font-size: 12px;
}

.result-label {
    margin-top: 0.5em;
    padding: 10px;
    font-size: 0.9rem;
    font-weight: bold;
}

.cropper {
  height: 400px;
}

button.choose-file-button {
    width: 200px;
    height: 40px;
    border-radius: 2px;
    background-color: #ffffff;
    border: solid 1px #7052CB;
    font-size: 13px;
    color: #7052CB;
    cursor: pointer;
}

button.analyze-button {
    width: 200px;
    height: 40px;
    border: solid 1px #7052CB;
    border-radius: 2px;
    background-color: #7052CB;
    font-size: 13px;
    color: #ffffff;
    cursor: pointer;
}

button.resubmit-button {
    width: 200px;
    height: 40px;
    border: solid 1px #5ccb52;
    border-radius: 2px;
    background-color: #5ccb52;
    font-size: 13px;
    color: #ffffff;
    cursor: pointer;
}

button:focus {
    outline: 0;
}
</style>
