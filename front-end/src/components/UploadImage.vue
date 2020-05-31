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
      <button v-if="!editImage" class='choose-file-button' type='button' @click="showPicker">Select Image</button>
      <div class='upload-label'>
        <label>{{ imageName ? imageName : 'No file chosen' }}</label>
      </div>
      <div>
        <img :class="imageUrl && !editImage ? '' : 'no-display'" alt='Chosen Image' height='400' :src="imageUrl">
      </div>

      <div class="image-edit-panel" v-if="editImage">
        <div class="image-field">
          <cropper
            v-if="mode === 'crop'"
            classname="cropper"
            :debounce="100"
            :src="imageUrl"
            @change="crop"
          ></cropper>
          <div :style="mode === 'blur' ? 'display: block' : 'display: none'">
            <canvas 
              ref="mainCanvas" 
              width=300 
              height=300 
              @mousedown="handleMouseDown"
              @mousemove="handleMouseMove"
              @mouseup="handleMouseUp"></canvas>
            <canvas id='tempCanvas' ref="tempCanvas" width=300 height=300 class="tmp-canvas"></canvas>
          </div>
          <div class="apply-edit">
            <button class='apply-button' type='button' @click="apply">
              {{ mode === 'crop' ? 'Apply cropping' : 'Apply blurring' }}
            </button>
            <button v-if="mode === 'blur'" class='clean-button' type='button' @click="clearBlur">
              Clean
            </button>
          </div>
        </div>
        <div class="tool-bar">
          <img class="tool" src="@/assets/crop.png" alt="crop" title="Crop image" height="23" @click="mode = 'crop'">
          <img class="tool" src="@/assets/blur.png" alt="blur" title="Blur image" height="23" @click="modeBlur()">
        </div>
      </div>

      <div 
        class='result-label' 
        :style="'color: ' + responseMsgColor">
        <label>{{responseMsg}}</label>
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
import { boxBlurCanvasRGBA } from '@/assets/FastBlur.js'

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
      mode: 'crop',
      imgBlur: null,
    }
  },
  methods: {
    apply () {
      if (this.mode === 'crop') {
        this.pickedImage = dataURLtoBlob(this.cropedImage)
        this.imageUrl = URL.createObjectURL(this.pickedImage)
      } else {
        this.pickedImage = dataURLtoBlob(this.canvas.toDataURL())
        this.imageUrl = URL.createObjectURL(this.pickedImage)
      }
    },
    clearBlur () {
      this.modeBlur()
    },
    modeBlur (image=null) {
      this.mode = 'blur'
      
      this.img = new window.Image()
      this.img.crossOrigin = "anonymous"
      this.img.src = image === null ? this.imageUrl : image

      this.img.onload = () => {
        this.canvas = this.$refs.mainCanvas
        this.tempCanvas = this.$refs.tempCanvas
        this.tempCtx = this.tempCanvas.getContext("2d")
        this.ctx = this.canvas.getContext("2d")

        this.width = this.img.width * (400 / this.img.height)
        this.canvas.width = this.tempCanvas.width = this.width
        this.canvas.height = this.tempCanvas.height = 400
        this.ctx.drawImage(this.img, 0, 0, this.width, 400)

        this.isDown = false;
        this.PI2 = Math.PI * 2;
      }
    },
    handleMouseDown (e) {
      e.preventDefault();
      e.stopPropagation();
      this.tempCtx.clearRect(0, 0, this.tempCanvas.width, this.tempCanvas.height);
      this.isDown = true;
    },
    handleMouseMove(e) {
      if (!this.isDown) {
          return
      }
      e.preventDefault();
      e.stopPropagation();
      let offsetX = this.canvas.getBoundingClientRect().left;
      let offsetY = this.canvas.getBoundingClientRect().top;
      let mouseX = parseInt(e.clientX - offsetX);
      let mouseY = parseInt(e.clientY - offsetY);
      this.ctx.beginPath();
      this.ctx.arc(mouseX, mouseY, 20, 0, this.PI2);
      this.ctx.closePath();
      this.ctx.fill();
      this.tempCtx.beginPath();
      this.tempCtx.arc(mouseX, mouseY, 20, 0, this.PI2);
      this.tempCtx.closePath();
      this.tempCtx.fill();
    },
    handleMouseUp(e) {
      e.preventDefault();
      e.stopPropagation();
      this.isDown = false;
      this.tempCtx.save();
      this.tempCtx.globalCompositeOperation = "source-in";
      this.tempCtx.drawImage(this.img, 0, 0, this.width, 400);
      this.tempCtx.restore();
      boxBlurCanvasRGBA("tempCanvas", 0, 0, this.tempCanvas.width, this.tempCanvas.height, 4, 0);
      this.ctx.save();
      this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);
      this.ctx.drawImage(this.tempCanvas, 0, 0, this.width, 400);
      this.ctx.globalCompositeOperation = "destination-over";
      this.ctx.drawImage(this.img, 0, 0, this.width, 400);
      this.ctx.restore();
      this.modeBlur(this.canvas.toDataURL())
    },
    crop({coordinates, canvas}) {
      this.cropedImage = canvas.toDataURL()
      console.log(coordinates)
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
                this.responseMsgColor = '#58B0F8'
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
                this.responseMsg = 'Crop out or blur the regions that could reveal identity'
                this.responseMsgColor = '#FEFEFE'
                this.mode = 'crop'
              } else {
                this.responseMsg = 'No identity detected'
                this.responseMsgColor = '#58B0F8'
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
    color: #FEFEFE;
}

.content {
    margin-top: 5em;
}

.analyze {
    margin-top: 1em;
    margin-bottom: 5em;
}

.upload-label {
    padding: 10px;
    font-size: 12px;
}

.result-label {
    margin-top: 3em;
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
    background-color: #19181F;
    border: solid 1px #6E39E8;
    font-size: 1.rem;
    color: #6E39E8;
    cursor: pointer;
    font-weight: bold;
}

button.analyze-button {
    width: 200px;
    height: 40px;
    border: solid 1px #6E39E8;
    border-radius: 2px;
    background-color: #6E39E8;
    font-size: 1.rem;
    color: #FEFEFE;
    cursor: pointer;
}

button.resubmit-button {
    width: 200px;
    height: 40px;
    border: solid 1px #58B0F8;
    border-radius: 2px;
    background-color: #58B0F8;
    font-size: 1.rem;
    color: #FEFEFE;
    cursor: pointer;
}

button.apply-button {
  margin-top: 0.5rem;
  width: 130px;
  height: 30px;
  border: solid 1px #d1d1d1;
  border-radius: 10px;
  background-color: #d1d1d1;
  font-size: 0.9rem;
  color: #19181F;
  cursor: pointer;
}

button.clean-button {
  margin-top: 0.5rem;
  margin-left: 0.5rem;
  width: 90px;
  height: 30px;
  border: solid 1px #d1d1d1;
  border-radius: 10px;
  background-color: #d1d1d1;
  font-size: 0.9rem;
  color: #19181F;
  cursor: pointer;
}

button:focus {
    outline: 0;
}

.image-edit-panel {
  margin-top: 1rem;
  display: flex;
  justify-content: center;
}

.tool-bar {
  display: flex;
  flex-direction: column;
}

.tool {
  margin-left: 10px;
  margin-bottom: 10px;
  cursor: pointer;
  background-color: #d1d1d1;
  padding: 0.2rem;
  border-radius: 0.2rem;
}

.tmp-canvas {
  position: absolute;
  top: -100%;
}
</style>
