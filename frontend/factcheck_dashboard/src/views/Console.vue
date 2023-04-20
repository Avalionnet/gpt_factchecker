<template>
  <div>
    <div class="pb-9 pt-3 pt-md-8 bg-gradient-dark">
      <b-container fluid>
        <b-row>
          <div class="hookWrapper mx-auto">
            <h1 class="hookContent">{{ hook }}</h1>
          </div>
        </b-row>
        <b-row>
          <div class="searchBar mx-auto">
            <b-form-group>
                <h4 id="input-label" style="margin-left: 3px;">Claim</h4>
              <b-input-group>
                <b-form-textarea 
                  class="formInput" 
                  id="query-input" 
                  v-model="claim" 
                  placeholder="search for a claim to verify its authenticity">
                </b-form-textarea>
                <b-input-group-append>
                  <!-- change @click back to decompClaim / tmpMethod -->
                  <b-button id="search-btn" @click="decompClaim">Verify</b-button>
                </b-input-group-append>
              </b-input-group>
              <b-input-group>
                <transition name="fade">
                  <div class="justificationInput mx-auto" v-if="isJustificationNeeded">
                    <b-row>
                      <h3 id="input-label">Justification</h3>
                    </b-row>
                    <b-row>
                      <b-form-textarea
                        id="justification-textarea"
                        placeholder="Add your justification paragraph here!"
                        v-model="justification"
                      ></b-form-textarea>
                    </b-row>
                    <b-row>
                      <b-button 
                        id="just-btn" 
                        variant="link" 
                        class="mx-auto" 
                        @click="isJustificationNeeded=false"
                      >- Justification Paragraph
                      </b-button>
                    </b-row>
                  </div>
                  <b-button 
                    id="just-btn" 
                    variant="link" 
                    class="mx-auto" 
                    v-if="!isJustificationNeeded" 
                    @click="isJustificationNeeded=true"
                  >+ Justification Paragraph
                  </b-button>
                </transition>
              </b-input-group>
            </b-form-group>
          </div>
        </b-row>
      </b-container>
    </div>
    <b-container fluid class="mt--7" v-if="stage == -1">
      <b-row>
        <b-col>
          <h2 style="text-align: center; margin-top: 0px; margin-bottom: 20px; color: white;">Let's Check these for a start 🧐</h2>
        </b-col>
      </b-row>
      <b-row>
        <b-card-group deck style="width: 92%; margin-left: 4%; margin-bottom: 70px;">
          <b-card v-for="(e, index) in exampleContent" :key="index" :title="e.title" :img-src="e.imgUrl" img-alt="Image" img-top>
            <b-card-text style="margin-bottom: 60px;">
              {{ e.claim }}
            </b-card-text>
            <b-button @click="letsCheckExample(e.claim)" variant="primary" style="position: absolute; bottom: 20px;">Let's Check</b-button>
          </b-card>
        </b-card-group>
      </b-row>
    </b-container>
    <!--Charts-->
    <b-container fluid class="mt--7">
      <!-- Print decomposition here -->
      <!-- <b-card class="mt-5  qsnResponse" v-html="response.replace(/\n/g, '<br>')">
      </b-card> -->
      <!--Tables-->
      <b-card class="mt-3 progressCard" v-if="stage >= 0">
        <el-steps :active="stage" finish-status="success" align-center style="min-width: 500px;">
          <el-step title="Stage 1" icon="el-icon-scissors"></el-step>
          <el-step title="Stage 2" icon="el-icon-edit-outline"></el-step>
          <el-step title="Stage 3" icon="el-icon-guide"></el-step>
          <el-step title="Stage 4" icon="el-icon-loading"></el-step>
          <el-step title="Stage 5" icon="el-icon-data-analysis"></el-step>
        </el-steps>
        <div v-if="stage == 0">
          <h1 class="mt-3">decomposing your claim</h1>
          <p>to better understand and fact-check the fine details involved</p>
          <b-spinner variant="primary"></b-spinner>
        </div>
        <div v-if="stage == 1">
          <h1 class="mt-3">review sub-questions</h1>
          <p>
            Please review and modify the decomposed sub-questions below. 
            <br>
            We will be fact checking the claim based on these sub-questions so do try to keep them 
            minimal and binary for better performance. 
            <br>
            <br>
            click <b><u>Continue</u></b> whenever you're ready 😉
          </p>
          <el-button type="primary" @click="stage = 2">Continue</el-button>
        </div>
        <div v-if="stage == 2">
          <h1 class="mt-3">crafting question hypothesis</h1>
          <p>converting your sub-questions to hypothesis for validation</p>
          <br>
          <div class="d-inline-block" style="min-width: 400px; display: inline-block;">
            <base-progress type="gradient-info" :value="stage2Prog" />
            <span class="mr-2">{{stage2Prog.toString()}}%</span>
          </div>
          <br><br>
          <b-spinner variant="primary"></b-spinner>
        </div>
        <div v-if="stage == 3">
          <h1 class="mt-3">verifying your claim</h1>
          <p>we're searching the web to verify your claim, hang tight 🎈</p>
          <br>
          <div class="d-inline-block" style="min-width: 400px; display: inline-block;">
            <base-progress type="gradient-info" :value="stage3Prog"/>
            <span class="mr-2">{{stage3Prog.toString()}}%</span>
          </div>
          <br><br>
          <b-spinner variant="primary"></b-spinner>
        </div>
        <div v-if="stage == 4">
          <h1 class="mt-3">FactCheck Results</h1>
          <h6><u>Overall Veracity Score</u></h6>
          <el-progress type="dashboard" :percentage="finalVeracityScore" :color="colors"></el-progress>
          <br>
          <el-popover trigger="hover" placement="top">
            <p class="hoverLabel"><b>Supporting Evidence:</b> {{ totalSupport }}</p>
            <p class="hoverLabel"><b>Refuting Evidence:</b> {{ totalRefute }}</p>
            <div slot="reference">
              <el-tag :type="finalVeracity === 'Mostly True' ? 'success' 
                                      : finalVeracity === 'Processing' ? 'primary' 
                                      : 'danger'"><b>{{ finalVeracity }}</b></el-tag>
            </div>  
        </el-popover>
        </div>
      </b-card>
      <b-row class="mt-3">
        <b-col>
          <question-table 
            :fact-check-data="subQsnJsonArr"
            :current-stage="stage"
            @s2Prog="updateStage2Prog"
            @s3Prog="updateStage3Prog"
            @convertSuccess="stage=3"
            @searchSuccess="stage=4"
            @results="processFactCheckResults"
          >
          </question-table>
        </b-col>
      </b-row>
      <!--End table-->
    </b-container>

  </div>
</template>
<script>
  // Import the axios library for making HTTP requests to replace the original AJAX calls
  import axios from 'axios';

  // Components
  import BaseProgress from '@/components/BaseProgress';
  import QuestionTable from './Dashboard/QuestionTable.vue';

  export default {
    components: {
      QuestionTable
    },
    data() {
      return {
        claim: "",
        justification: "",
        hook: "|",
        hookList: ["WE'RE SIMPLIFYING AUTOMATED FACT-CHECKING", "WE'RE THE SEARCH ENGINE FOR THE TRUTH" ,"IT'S AS EASY AS SEARCHING FOR A CLAIM", "REDISCOVER THE TRUTH"],
        response: "",
        subQsnJsonArr: [],
        stage: -1,
        stage2Prog: 0,
        stage3Prog: 0,
        isJustificationNeeded: false,
        finalVeracityScore: 0,
        finalVeracity: "Processing",
        totalSupport: 0,
        totalRefute: 0,
        exampleContent: [
          {
            title: "China-Taiwan Relations",
            imgUrl: "https://images.theconversation.com/files/482947/original/file-20220906-26-k6jhsl.png?ixlib=rb-1.1.0&rect=2%2C0%2C982%2C554&q=45&auto=format&w=926&fit=clip",
            claim: "China staged war games around Taiwan in August after then-Speaker Nancy Pelosi visited Taipei, and has continued military activities near Taiwan, though on a reduced scale. Separately, 10 Chinese aircraft crossed the median line on Friday carrying out combat readiness patrols, a move that Taiwan's defence ministry said has \"deliberately created tension\" and undermined peace and stability."
          },
          {
            title:"Donald Trump Jr Indicted",
            imgUrl: "https://ichef.bbci.co.uk/live-experience/cps/1440/cpsprodpb/11E75/production/_129233337_trump-hero-gettyimages-1473376926.jpg",
            claim: "Donald J. Trump is the first former US president to have been indicted. Trump won't be in handcuffs when he appears in court but will have his fingerprints and a mugshot taken, and be brought before a judge."
          },
          {
            title: "Turkey's Earthquake",
            imgUrl: "https://www.japantimes.co.jp/wp-content/uploads/2023/02/np_file_209343.jpeg",
            claim: "The two powerful earthquakes that hit Turkey and Syria on 6 February 2023 were of similar magnitude (7.8 and 7.6) and only nine hours apart. These events are referred to as an earthquake doublet because they are a pair of powerful earthquakes that have centroids closer than their rupture size and occur within a time frame that is shorter than the recurrence time inferred from the plate motion."
          },
          {
            title: "Finland joins NATO",
            imgUrl: "https://ichef.bbci.co.uk/news/976/cpsprodpb/15F74/production/_129227998_fa384709714485f0ce08f9db93f83ce428a227350_0_3608_24161000x670.jpg.webp",
            claim: "Finland will become the 31st member of Nato after Turkey's parliament voted to approve its application. Finland is now set to become the seventh Nato country on the Baltic Sea, further isolating Russia's coastal access at St Petersburg and on its small exclave of Kaliningrad."
          }
        ],
        colors: [
          {color: '#f56c6c', percentage: 30},
          {color: '#e6a23c', percentage: 40},
          {color: '#1989fa', percentage: 50},
          {color: '#6f7ad3', percentage: 70},
          {color: '#5cb87a', percentage: 100}
        ],
      };
    },
    async mounted() {
      let i = 0;
      while(true) {
        if(i < this.hookList.length) {
          await this.hookTyper(this.hookList[i]);
          await this.hookDeleter();
          i++
        } else {
          i = 0;
        }
      }
    },
    methods: {
      retrieveEvidence() {
        // Set the URL for the API request
        const url = 'https://empty-meadow-488.fly.dev/api2';

        // Make the API request using axios
        axios.get(url, {
          params: {
            query: this.claim
          }
        })
        .then(response => {
            console.log(response.data);
        })
        .catch(error => {
            console.log(error);
        });
      },
      decompClaim() {
        this.stage = 0;
        const url = 'https://decomp-hnozmogerq-as.a.run.app/decomp';
        axios.get(url, {
          params: {
            claim: this.claim,
          }
        })
        .then(response => {
            console.log(response.data);
            this.processRawQuestions(response.data);
        })
        .catch(error => {
            console.log(error);
            this.decompClaim();
        });
      },
      async hookTyper(text) {
        let i = 0;
        let j = 0;
        let speed = 80;
        while (i < text.length) {
          this.hook = this.hook.slice(0, -1)
          this.hook += text.charAt(i) + "|";
          i++;
          await new Promise(r => setTimeout(r, speed));
        }
        while (j < 7) {
          this.hook = this.hook.slice(0, -1)
          await new Promise(r => setTimeout(r, 500));
          this.hook += "|";
          await new Promise(r => setTimeout(r, 500));
          j++;
        }
      },
      async hookDeleter() {
        let speed = 80;
        while (this.hook.length > 1) {
          this.hook = this.hook.slice(0, -2)
          this.hook += "|";
          await new Promise(r => setTimeout(r, speed));
        }
      },
      processRawQuestions(rawResponse) {
        try{
          rawResponse = rawResponse.trim();
          var subQsnArr = rawResponse.split("\n");
          subQsnArr = subQsnArr.map(str => str.substring(str.indexOf(".") + 2));
          this.subQsnJsonArr = [];
          // Create Json Array for sub questions
          for(let i = 0; i < subQsnArr.length; i++) {
            var subQsnObject = {
              idx: i,
              question: subQsnArr[i].trim(),
              evidence: "Searching",
              verdict: "Processing",
              truthScore: 0,
              refuting: 0,
              supporting: 0,
              progressType: "gradient-info",
              showEvidence: false,
            };
            if (subQsnObject.question != "") {
              this.subQsnJsonArr.push(subQsnObject);
              this.stage = 1;
              // To remove
              this.response += subQsnArr[i] + "\n";
            }
          }
        } catch (error) {
          console.log(error);
        }
      },
      processFactCheckResults(support, refute) {
        this.totalSupport = parseInt(support);
        this.totalRefute = parseInt(refute);

        let score = Math.round((support / (support+refute)) * 100);
        
        this.finalVeracityScore = isNaN(score) ? 0 : score;
        this.finalVeracity = this.finalVeracityScore >= 50 ? "Mostly True" : "Mostly False";
      },
      updateStage2Prog(val) {
        this.stage2Prog = val;
      },
      updateStage3Prog(val) {
        this.stage3Prog = val;
      },
      letsCheckExample(egClaim) {
        this.claim = egClaim;
        this.decompClaim();
      },
      tmpMethod() {
        const fakeData = "1. Russian military paratroopers landed in Ukraine\n2. Hitler won world war 2\n3. Donald Trump was arrested on Monday following an assualt";
        this.processRawQuestions(fakeData);
      }
    },
  };
</script>
<style>
.hookContent {
  color: white;
  font-size: 40px;
  margin-top: 100px;
  margin-bottom: 25px;
  text-align: left;
}

#input-label {
  color: white;
}

.searchBar {
  width: 60%;
}

#query-input {
  width: 50%;
  height: 40px;
  margin-left: 5px;
  margin-right: 20px;
  border-radius: 10px;
}

#search-btn {
  border-radius: 8px;
  padding: 1px 18px;
  background-color: #282A36;
  border: none;
  color: white;
  font-size: 100%;
  transition-duration: 0.2s;
  /* margin-left: 10px; */
  box-shadow: 0px 0px 0.5px 0.5px rgba(255,184,108,0.6), 0px 0px 2px 2px rgba(255,184,108,0.19);
  color:#FFB86C;
}

#search-btn:hover {
  background-color:#FFB86C;
  color: #282A36;
}

#just-btn {
  color: #FFB86C;
}

.justificationInput {
  width: 95%;
  margin-top: 20px;
}

#justification-textarea {
  border-radius: 12px;
}

.qsnResponse {
  padding: 15px;
}

.progressCard {
  align-items: center;
  text-align: center;
}

.hoverLabel {
  font-size: 12px;
  font-weight: 400;
}

.formInput {
  border-radius: 8px;
  border-color: none;
  padding: 0.8vh 0.8vw;
  width: 80%;
  border: 0;
  transition: .3s border-color;
  background-color: white;
  margin-bottom: 0.4vh;
  color: #282A36;
}
.formInput:focus {
  border-radius: 8px;
  padding: 0.8vh 0.8vw;
  border: 0;
  transition: .3s border-color;
  border: 1px solid #FFB86C;
  color: #282A36;
}
.formInput:hover {
  border: #282A36;
  box-shadow: 0px 0px 1px 1px rgba(255,184,108,0.6), 0px 0px 2px 2px rgba(255,184,108,0.19);
}
.formInput::placeholder {
  padding-top: 0px;
  margin-bottom: 2px;
  padding-left: 1px;
}

.fade-enter-active, .fade-leave-active {
  transition: opacity 0.5s;
}

.fade-enter, .fade-leave-to {
  opacity: 0;
}
</style>
