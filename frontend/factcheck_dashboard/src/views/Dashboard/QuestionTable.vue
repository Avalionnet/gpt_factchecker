<template>
  <div class="mainContentWrapper" v-if="currentStage > 0">
    <b-container fluid class="containerWrapper">
      <b-row no-gutters>
        <b-col xl="7" class="mb-5 mb-xl-0">
          <b-card body-class="p-0" header-class="border-0" class="tableContainer">
            <template v-slot:header>
              <b-row align-v="center">
                <b-col>
                  <h3 class="mb-0">{{ tableTitle }}</h3>
                </b-col>
                <b-col class="text-right">
                  <base-button v-if="currentStage == 1" @click="addQuestion" size="sm" type="primary">+ Sub-Question</base-button>
                </b-col>
              </b-row>
            </template>

            <el-table
              class="table-responsive table"
              :data="factCheckData.filter(data => !searchInput || data.question.toLowerCase().includes(searchInput.toLowerCase()))"
              header-row-class-name="thead-light"
              highlight-current-row
              @current-change="displayEvidence"
              ref="subQsnTable"
              style="border-collapse: collapse;"
              >
              
              <el-table-column label="ID" width="30%" prop="idx" :cell-style="{padding: '2px'}">
                <template v-slot="{row}">
                  <div class="font-weight-600">{{row.idx + 1}}</div>
                </template>
              </el-table-column>

              <el-table-column label="Sub-Question" min-width="185%" prop="question">
                <template v-slot="{row}">
                  <div class="font-weight-600" v-if="expandedRow != row.idx">{{row.question}}</div>
                  <el-input v-model="replacement" v-if="expandedRow == row.idx"></el-input>
                </template>
              </el-table-column>

              <el-table-column
                align="right"
                v-if="currentStage == 1"
                :cell-style="{padding: '5px'}">
                <template slot="header" slot-scope="scope">
                  <el-input
                    v-model="searchInput"
                    size="mini"
                    placeholder="Type to search"/>
                </template>
                <template slot-scope="scope">
                  <el-button
                    size="mini"
                    @click="toggleEdit(scope.$index)" v-if="!isEditing && expandedRow != scope.$index">Edit</el-button>
                  <el-button
                    size="mini"
                    type="success"
                    @click="saveEdit(scope.$index)" v-if="isEditing && expandedRow == scope.$index">Save</el-button>
                  <el-button
                    size="mini"
                    type="danger"
                    @click="deleteRow(scope.$index)">Delete</el-button>
                </template>
              </el-table-column>

              <!-- Columns to display final results -->

              <el-table-column label="Verdict" width="140px" prop="verdict" v-if="currentStage >= 2">
                <template v-slot="{row}">
                  <el-popover trigger="hover" placement="right">
                    <p class="hoverLabel"><b>Supporting Evidence:</b> {{ row.supporting }}</p>
                    <p class="hoverLabel"><b>Refuting Evidence:</b> {{ row.refuting }}</p>
                    <div slot="reference">
                      <el-tag :type="row.verdict === 'likely true' ? 'success' 
                                        : factCheckData[evidenceToDisplay].verdict === 'Processing' ? 'primary' 
                                        : 'danger'"><b>{{ row.verdict }}</b></el-tag>
                    </div>
                  </el-popover>
                </template>
              </el-table-column>

              <el-table-column label="Truth Score" prop="truthScore" min-width="120" v-if="currentStage >= 2" :cell-style="{padding: '2px'}">
                <template v-slot="{row}">
                  <div class="d-flex align-items-center">
                    <span class="mr-2">{{row.truthScore}}%</span>
                    <base-progress :type="row.progressType" :value="row.truthScore" />
                  </div>
                </template>
              </el-table-column>

            </el-table>
          </b-card>
        </b-col>
        <b-col xl="5" class="mb-5 mb-xl-0" v-if="currentStage >= 2">
          <b-container class="evidenceContainer">
            <b-card>
              <h2>Supporting Evidence</h2>
              <h4><u>Sub-Claim Hypothesis:</u><br> {{ factCheckData[evidenceToDisplay].question }}</h4>
              <el-popover trigger="hover" placement="left">
                <p class="hoverLabel"><b>Supporting Evidence:</b> {{ factCheckData[evidenceToDisplay].supporting }}</p>
                <p class="hoverLabel"><b>Refuting Evidence:</b> {{ factCheckData[evidenceToDisplay].refuting }}</p>
                <div slot="reference">
                  <el-tag :type="factCheckData[evidenceToDisplay].verdictLabel"><b>{{ factCheckData[evidenceToDisplay].verdict }}</b></el-tag>
                </div>
              </el-popover>
            </b-card>
            <b-card class="mt-3" v-for="(e, index) in factCheckData[evidenceToDisplay].evidence" :key="index" v-if="currentStage === 4">
              <a :href="e.url" target="_blank">
                <h4 class="cardTitle">{{ e.title }}</h4>
              </a>
              <el-tag :type="e.nli_class === 'entailment' ? 'success' : 'danger'"
                                    ><b>{{ processNliClass(e.nli_class) }}</b></el-tag>
              <p><b><u>Relevant Article Extract:</u></b></p>
              <p>... <span v-html="e.snippet"></span> ...</p>
            </b-card>
          </b-container>
        </b-col>
      </b-row>
    </b-container>
  </div>
</template>
<script>
  import { BaseProgress } from '@/components';
  import { Table, TableColumn, DropdownMenu, DropdownItem, Dropdown} from 'element-ui'
  import axios from 'axios';


  export default {
    name: 'question-table',
    props: {
      factCheckData: {
        type: Array,
        default: () => []
      },
      currentStage: Number,
    },
    components: {
      BaseProgress,
      [Table.name]: Table,
      [TableColumn.name]: TableColumn,
      [Dropdown.name]: Dropdown,
      [DropdownItem.name]: DropdownItem,
      [DropdownMenu.name]: DropdownMenu,
    },
    data() {
      return {
        isEditing: false,
        tableTitle: "Decomposed Questions",
        searchInput: "",
        expandedRow: -1,
        replacement: "",
        quinResults: [],
        numOfCompletedConversion: 0,
        numOfCompletedSearch: 0,
        evidenceToDisplay: 0,
        totalSupport: 0,
        totalRefute: 0,
      }
    },
    watch: {
      currentStage: function(newVal, oldVal) {
        if(newVal == 2) {
          this.tableTitle = "Sub-Claim Hypothesis"
          this.numOfCompletedConversion = 0;
          for(let i = 0; i < this.factCheckData.length; i++) {
            this.hypothesizeSubQuestion(this.factCheckData[i].question, i);
          }
        }
      },
      numOfCompletedConversion: function(newVal, oldVal) {
        let prog = Math.round(newVal/this.factCheckData.length*100);
        console.log("Stage 2 Prog: " + prog.toString());
        this.$emit('s2Prog', prog);
        if(newVal == this.factCheckData.length) {
          this.$emit('convertSuccess');
          this.executeStage3();
        }
      },
      numOfCompletedSearch: function(newVal, oldVal) {
        let prog = Math.round(newVal/this.factCheckData.length*100);
        console.log("Stage 3 Prog: " + prog.toString());
        this.$emit('s3Prog', prog);
        if(newVal == this.factCheckData.length) {
          this.updateFactCheckData();
          this.sanitizeResponse();
          this.computeOverallVeracity();
          this.$emit('searchSuccess')
        }
      }
    },
    methods: {
      displayEvidence(obj) {
        // obj is the json object of the selected table row
        this.evidenceToDisplay = obj.idx;
      },
      deleteRow(rowIndex) {
        this.factCheckData.splice(rowIndex, 1);
      },
      toggleEdit(rowIndex) {
        this.replacement = this.factCheckData[rowIndex].question;
        this.expandedRow = rowIndex;
        this.isEditing = true;
      },
      saveEdit(rowIndex) {
        this.factCheckData[rowIndex].question = this.replacement;
        this.expandedRow = -1;
        this.replacement = "";
        this.isEditing = false;
      },
      async executeStage3() {
        this.quinResults = new Array(this.factCheckData.length).fill();
        this.numOfCompletedSearch = 0;
        console.log(this.quinResults);
        for(let i = 0; i < this.factCheckData.length; i++) {
          await this.retrieveEvidence(this.factCheckData[i].question, i);
          // await new Promise(resolve => setTimeout(resolve, 3000));
        }
      },
      hypothesizeSubQuestion(subQ, idx) {
        this.stage = 0;
        const url = 'https://hypothesize-hnozmogerq-as.a.run.app/hypothesize';
        axios.get(url, {
          params: {
            question: subQ,
          }
        })
        .then(response => {
            console.log(response.data);
            this.factCheckData[idx].question = response.data;
            this.numOfCompletedConversion++;
        })
        .catch(error => {
            console.log(error);
        });
      },
      retrieveEvidence(claim, idx) {
        // Set the URL for the API request
        const url = 'https://empty-meadow-488.fly.dev/api2';

        // Make the API request using axios
        axios.get(url, {
          params: {
            query: claim
          }
        })
        .then(response => {
            // console.log(response.data);
            this.quinResults[idx] = response.data;
            this.quinResults[idx].question = claim;
            this.numOfCompletedSearch += 1;
            console.log(this.quinResults);
        })
        .catch(error => {
            console.log(error);
            this.retrieveEvidence(claim, idx);
        });
      },
      updateFactCheckData() {
        for(let i = 0; i < this.factCheckData.length; i++) {
          let totalVal = this.quinResults[i].data.refuting + this.quinResults[i].data.supporting;
          this.factCheckData[i].refuting = this.quinResults[i].data.refuting !== undefined ? this.quinResults[i].data.refuting : 0;
          this.factCheckData[i].supporting = this.quinResults[i].data.supporting !== undefined ? this.quinResults[i].data.supporting : 0;
          this.factCheckData[i].evidence = this.quinResults[i].data.results;
          this.factCheckData[i].truthScore = this.factCheckData[i].evidence.length !== 0 && totalVal !== 0 
                                                ? Math.round(this.factCheckData[i].supporting / totalVal * 100)
                                                : 0;
          this.factCheckData[i].verdict = totalVal == 0 ? "unknown" : this.factCheckData[i].truthScore >= 50 ? "likely true" : "likely false";
          this.factCheckData[i].verdictLabel = totalVal == 0 ? "dark" : this.factCheckData[i].truthScore >= 50 ? "success" : "danger";
        }
      },
      sanitizeResponse() {
        for(let i = 0; i < this.factCheckData.length; i++) {
          for(let j = 0; j < this.factCheckData[i].evidence.length; j++) {
            this.factCheckData[i].evidence[j].title = this.factCheckData[i].evidence[j].title.replace(/\\x([0-9A-Fa-f]{2})/g, "");
            this.factCheckData[i].evidence[j].snippet = this.factCheckData[i].evidence[j].snippet.replace(/\\x([0-9A-Fa-f]{2})/g, "");
            this.factCheckData[i].evidence[j].evidence = this.factCheckData[i].evidence[j].evidence.replace(/\\x([0-9A-Fa-f]{2})/g, "");
          }
        }
      },
      computeOverallVeracity() {
        this.totalSupport = 0;
        this.totalRefute = 0;
        for(let i = 0; i < this.factCheckData.length; i++) {
          if (this.factCheckData[i].supporting !== undefined) {
            this.totalSupport += parseInt(this.factCheckData[i].supporting);
          }
          if (this.factCheckData[i].refuting !== undefined) {
            this.totalRefute += parseInt(this.factCheckData[i].refuting);
          }
        }
        this.$emit('results', this.totalSupport, this.totalRefute);
      },
      processNliClass(resp) {
        if (resp == "entailment") {
          return "Support"
        } else if (resp == "contradiction") {
          return "Refutes"
        } else {
          return "Unclassified"
        }
      },
      addQuestion() {
        var subQsnObject = {
              idx: this.factCheckData.length,
              question: "",
              evidence: "Searching",
              verdict: "Processing",
              truthScore: 0,
              refuting: 0,
              supporting: 0,
              progressType: "gradient-info",
              showEvidence: false,
            };
            this.factCheckData.push(subQsnObject);
            this.toggleEdit(this.factCheckData.length - 1);
      },
      retrieveEvidence2(orignalClaim, subQsns, idx) {
        // Set the URL for the API request
        const url = 'https://empty-meadow-488.fly.dev/api2';

        // Make the API request using axios
        axios.get(url, {
          params: {
            query: originalClaim,
            subq: subQsns //Contains the array of sub-questions
          }
        })
        .then(response => {
            // console.log(response.data);
            this.quinResults[idx] = response.data;
            this.quinResults[idx].question = claim;
            this.numOfCompletedSearch += 1;
            console.log(this.quinResults);
        })
        .catch(error => {
            console.log(error);
        });
      },
    },
  };
</script>
<style>

.mainContentWrapper {
  padding: 0px;
  margin: 0px;
  width: 90vw;
}

.containerWrapper {
  padding: 0px;
  width: 100%;
  margin-left: -40px;
  margin-right: 0px;
}

.tableContainer {
  max-height: 100vh;
  overflow-y: auto;
}

.evidenceContainer {
  height: 100vh;
  width: 130%;
  overflow: auto;
}

.evidenceCard {
  width: 95%;
  margin-left: 5%;
  margin-bottom: 20px;
}

.cardTitle {
  color: #1434A4;
}

.hoverLabel {
  font-size: 12px;
  font-weight: 400;
}

</style>
