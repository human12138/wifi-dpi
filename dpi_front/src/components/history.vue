<template>
  <div>
    <h1><Tooltip content='AP名称'>{{ap_name}}</Tooltip>的历史记录</h1>
    <Divider />
    <div id="d1">
      <div style="padding: 20px width:300px">
      <Card>
          <p slot="title" style="height:40px">
            <Icon type="ios-wifi"/>
            AP基本信息
            </p>
            <table style="text-align:left">
              <tr v-for="ap in ap_info"><td>{{ap.info_name}}</td><td>{{ap.info_data}}</td></tr>
              <tr>
                <td>查询日期范围:</td>
                <td>
                  <p v-model="showdate">{{showdate}}
                  <Dropdown @on-click="datechoose" trigger="custom" :visible="visible">
                    <a href="javascript:void(0)" @click="dropopen">
                        选择范围
                        <Icon type="ios-arrow-down"></Icon>
                    </a>
                    <DropdownMenu slot="list">
                        <DropdownItem name='1'>一周</DropdownItem>
                        <DropdownItem name='2'>一个月</DropdownItem>
                        <DropdownItem name='3'>三个月</DropdownItem>
                        <DropdownItem name='4'>六个月</DropdownItem>
                        <DropdownItem name='5'>一年</DropdownItem>
                        <DropdownItem name='6'>
                          <DatePicker
                            :open="open"
                            :value="value3"
                            confirm
                            type="daterange"
                            @on-change="handleChange"
                            @on-clear="handleClear"
                            @on-clickoutside='handleClear'
                            @on-ok="handleOk"
                            v-model="dates">
                            <a href="javascript:void(0)" @click='handleClick'>
                                <Icon type="ios-calendar-outline"></Icon>
                                <template>自定义范围</template>
                            </a>
                          </DatePicker>
                        </DropdownItem>
                    </DropdownMenu>
                  </Dropdown>
                </p></td></tr>
            </table>
      </Card>
    </div>
    <div style="width:50%">
        <Table border :height="300" :columns="columns1" :data="data1"  ></Table>
    </div>
  </div>
    <Divider />
      <div id='d1'>
        <div :class="className" :id="id" :style="{height:height,width:width}" ref="srcEchart"></div>
        <div :class="className" :id="id" :style="{height:height,width:width}" ref="desEchart"></div>

      <div id="main" style="width: 300px;height: 400px;float: right;display: inline-block;"></div>
    </div>
  </div>
</template>
<style>
#d1{
    display: -webkit-flex;
    display: flex;
    justify-content: space-around;
}
</style>
<script>
import echarts from 'echarts'
export default {
  props: {
    className: {
      type: String,
      default: 'yourClassName'
    },
    id: {
      type: String,
      default: 'yourID'
    },
    width: {
      type: String,
      default: '300px'
    },
    height: {
      type: String,
      default: '300px'
    },
    float: {
      type: String,
      default: 'left'
    }
  },
  mounted() {
    //this.getdata(this.$route.query.start_date,this.$route.query.stop_date);
    this.drawDes(),
    this.drawSrc(),
    this.drawPie('main')
  },
  beforeDestroy() {
    if (!this.chart) {
      return
    }
    this.chart.dispose();
    this.chart = null;
  },
  name: '',

  data () {
    return {
      visible: false,
      dates: '',
      open: false,
      value3: '',
      showdate: '一周内',
      modal1: false,
      flag: 0,
      //srcdata_x: '',
      //srcdata_y: '',
      //desdata_x: '',
      //desdata_y: '',
      ap_info: this.$route.query.ap_info,
      ap_name: this.$route.query.ap_info[0]['info_data'],

      columns1: [
        {
          title:'曾连接此AP的STA',
          key: 'sta_history',
          align: 'center',
          children:[
          {
            title: 'STA的MAC地址',
            key: 'mac'
          },
          {
            title: 'STA的IP地址',
            key: 'ip'
          },
          {
            title: '最近出现时间',
            key: 'date',
            tooltip: true
          },
          {
            title: '操作',
            key: 'action',
            width: '75',
            render: (h,params)=>{
              return h('Button',{
                props:{
                  type: 'primary',
                  size: 'small'
                },
                on:{
                  click: ()=>{
                    this.choose(params.index)
                  }
                }
              },'详情')
            }
          }
        ]
      }],
      //data1: [],
      charts: '',
      //opinion:'',
      //opinionData:''
      data1:[
        {ip: '192.168.3.126',mac:'D4:EE:07:32:01:5A',date: this.timeFormate()},
        {ip: '192.168.3.103',mac:'D4:EE:07:32:01:5A',date: this.timeFormate()},
        {ip: '192.168.3.2',mac:'D4:EE:07:32:01:5A',date: this.timeFormate()},
        {ip: '192.168.3.3',mac:'D4:EE:07:32:01:5A',date: this.timeFormate()},
      ],
      opinion:['HTTP','DNS','SSL','DHCP','Unknow','HTTP1','DNS1','SSL1','DHCP1','Unknow1'],
      opinionData:[
        {value:335, name:'HTTP'},
        {value:310, name:'DNS'},
        {value:234, name:'DHCP'},
        {value:135, name:'Unknow'},
        {value:1548, name:'SSL'},
        {value:335, name:'HTTP1'},
        {value:310, name:'DNS1'},
        {value:234, name:'DHCP1'},
        {value:135, name:'Unknow1'},
        {value:1548, name:'SSL1'}
      ],

      srcdata_x : [10, 52, 200, 334, 390, 330, 220,10, 52, 200],
      srcdata_y : ['D4:EE:07:32:01:5A', 'D4:EE:07:32:01:5B', 'D4:EE:07:32:01:5C', 'D4:EE:07:32:01:5D',
      'D4:EE:07:32:01:5C','D4:EE:07:32:01:5E', 'D4:EE:07:32:01:5F','D4:EE:07:32:01:5G','D4:EE:07:32:01:5H', 'D4:EE:07:32:01:5I'],
      desdata_x : [10, 52, 200, 334, 390, 330, 220, 200, 334, 390],
      desdata_y : ['192.168.199.126', '192.168.199.124', '192.168.1.3', '192.168.1.2',
      '192.168.3.6','192.168.199.103', '192.168.3.1', '192.168.199.124', '192.168.1.3', '192.168.1.2'],
    }
   },
  methods: {
    getdata: function(start,stop){
      let s = this
      this.$axios.get('gethistory',{
        params:{
          start_date: start,
          stop_date: stop
        }
      })
      .then(function(response){
          //alert(response.data['prot_x']);
          s.opinion = response.data['prot_x'];
          s.opinionData =response.data['prot_y'];
          s.srcdata_x = response.data['srcdata_x'];
          s.srcdata_y = response.data['srcdata_y'];
          s.desdata_x = response.data['desdata_x'];
          s.desdata_y = response.data['desdata_y'];
          s.data1 = response.data['ip'];
          s.drawPie('main');
          s.drawSrc();
          s.drawDes();
      });
    },
    drawDes: function() {
      this.chart = echarts.init(this.$refs.desEchart);
      // 把配置和数据放这里
      this.chart.setOption({
        color: ['#3398DB'],
        title: {
          text:'服务器流量',
          subtext: '',
          x:'center',
          textStyle:{
            color:"#222",
            fontStyle:"normal",
            fontWeight:"600",
            fontFamily:"san-serif",
            fontSize:16,
          }
        },

        tooltip: {
          trigger: 'axis',
          axisPointer: { // 坐标轴指示器，坐标轴触发有效
            type: 'line' // 默认为直线，可选为：'line' | 'shadow'
          }
        },
        grid: {
          left: '3%',
          right: '4%',
          bottom: '3%',
          containLabel: true
        },
        yAxis: [{
          type: 'category',
          data: this.desdata_y,
          axisTick: {
            alignWithLabel: true
          }
        }],
        xAxis: [{
          type: 'value'
        }],
        series: [{
          name: '服务器流量',
          type: 'bar',
          barWidth: '60%',
          data: this.desdata_x,
        }]
      })

    },
    drawSrc: function() {
      this.chart = echarts.init(this.$refs.srcEchart);
      // 把配置和数据放这里
      this.chart.setOption({
        color: ['#3398DB'],
        title: {
          text:'客户端流量',
          subtext: '',
          x:'center',
          textStyle:{
            color:"#222",
            fontStyle:"normal",
            fontWeight:"600",
            fontFamily:"san-serif",
            fontSize:16,
          }
        },

        tooltip: {
          trigger: 'axis',
          axisPointer: { // 坐标轴指示器，坐标轴触发有效
            type: 'line' // 默认为直线，可选为：'line' | 'shadow'
          }
        },
        grid: {
          left: '3%',
          right: '4%',
          bottom: '3%',
          containLabel: true
        },
        yAxis: [{
          type: 'category',
          data: this.srcdata_y,
          axisTick: {
            alignWithLabel: true
          }
        }],
        xAxis: [{
          type: 'value'
        }],
        series: [{
          name: '客户端流量',
          type: 'bar',
          barWidth: '60%',
          data: this.srcdata_x,
        }]
      })

    },
    drawPie: function(id){
      this.charts = echarts.init(document.getElementById(id))
      this.charts.setOption({
        title: {
          text:'协议分布',
          subtext: '',
          x:'center',
          textStyle:{
            color:"#222",
            fontStyle:"normal",
            fontWeight:"600",
            fontFamily:"san-serif",
            fontSize:16,
          }
        },
        tooltip: {
          trigger: 'item',
          formatter: '{a}<br/>{b}:{c} ({d}%)'
        },
        legend: {
          orient: 'horizontal',
          x: 'left',
          bottom: 0,
          data:this.opinion
        },
        series: [
          {
          name:'访问来源',
          type:'pie',
          radius:['50%','70%'],
          avoidLabelOverlap: false,
          label: {
            normal: {
              show: false,
              position: 'center'
            },
            emphasis: {
              show: true,
              textStyle: {
                fontSize: '30',
                fontWeight: 'blod'
              }
            }
          },
          labelLine: {
            normal: {
              show: false
            }
          },
            data:this.opinionData
          }
        ]
      })
    },

    choose: function(index){
      this.$router.push({
        path: '/parserinfo',
        query:{
          ip : this.data1[index].ip,
          mac: this.data1[index].mac
        }
      })
    },
    help: function(){
      this.modal1 = true
    },
    timeFormate: function() {
      let year = new Date(new Date()).getFullYear();
      let month =new Date(new Date()).getMonth() + 1 < 10? "0" + (new Date(new Date()).getMonth() + 1): new Date(new Date()).getMonth() + 1;
      let date =new Date(new Date()).getDate() < 10? "0" + new Date(new Date()).getDate(): new Date(new Date()).getDate();
      let hh =new Date(new Date()).getHours() < 10? "0" + new Date(new Date()).getHours(): new Date(new Date()).getHours();
      let mm =new Date(new Date()).getMinutes() < 10? "0" + new Date(new Date()).getMinutes(): new Date(new Date()).getMinutes();
      let ss =new Date(new Date()).getSeconds() < 10? "0" + new Date(new Date()).getSeconds(): new Date(new Date()).getSeconds();
      let time = year + "-" + month + "-" + date +" "+hh+":"+mm+":"+ss;
      return time;
    },
    handleClick () {
      this.open = true;
    },
    handleChange (date) {

    },
    handleClear () {
        this.open = false;
        this.visible=false;
    },
    handleOk () {
        this.showdate = this.datechange(this.dates[0])+"-"+this.datechange(this.dates[1]);
        this.open = false;
        this.visible = false;
    },
    dropopen (){
      this.visible=true;
    },
    datechoose:function(name){
      if(name=='1'){
        this.showdate = '一周';
        this.visible=false;
      }
      else if (name=='2') {
        this.showdate = '一个月';
        this.visible=false;
      }
      else if (name=='3') {
        this.showdate = '三个月';
        this.visible=false;
      }
      else if (name=='4') {
        this.showdate = '六个月';
        this.visible=false;
      }
      else if (name=='5') {
        this.showdate = '一年';
        this.visible=false;
      }
      else if (name=='6') {

      }
    },
    datechange: function(date){
        var month = date.getMonth()+1;
        var year = date.getFullYear();
        var day = date.getDate();
        var d = year+"/"+month+"/"+day;
        return d;
    },
  }
}
</script>
