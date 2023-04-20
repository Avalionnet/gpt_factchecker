<template>
  <footer class="footer">
    <b-row align-v="center" class="justify-content-lg-between">
      <b-col lg="4">
        <div class="copyright text-center text-lg-left text-muted">
          © Copyright {{year}}<a href="https://letscheck.nus.edu.sg/index.html" class="font-weight-bold ml-1" target="_blank">LET'S CHECK</a>
        </div>
      </b-col>
      <b-col lg="4">
        <div class="copyright text-center text-lg-center text-muted">
          powered by<a href="https://github.com/algoprog/Quin" class="font-weight-bold ml-1" target="_blank">Quin</a>
        </div>
      </b-col>
      <b-col lg="4">
        <b-nav align="center" class="nav-footer justify-content-lg-end">
          <b-nav-item href="https://ctic.nus.edu.sg/" target="_blank">
            Organization
          </b-nav-item>
        </b-nav>
      </b-col>
    </b-row>
  </footer>
</template>
<script>
export default {
  data() {
    return {
      year: new Date().getFullYear()
    };
  }
};
</script>
<style>
.footer {
  margin-top: 30px;
  padding-top: 15px;
  padding-bottom: 15px;
  padding-left: 20px;
  padding-right: 20px;
  height: 70px;
}
</style>
