<template>
  <div>
    <h1>深度包解析<a icon="ios-help"></a></h1>
    <Divider />
    <div id="d1">
        <div style="padding: 20px width:300px">
        <Card>
            <p slot="title" style="height:40px">
              <Icon type="ios-wifi"/>
              AP基本信息
                <Button id='name' @click="choose_ap" type="primary">切换AP</Button>
                <Modal v-model="modal1"
                title="选择AP"
                @on-ok="ok">
                <div id="container1" :style="{height:height,width:width}"></div>
                </Modal>
              </p>
            <table style="text-align:left">
              <tr v-for="ap in ap_info"><td>{{ap.info_name}}</td><td>{{ap.info_data}}</td></tr>
              <tr><td>操作:</td><td><Button id="id_search" type="primary" @click="history">查询AP历史</Button></td></tr>
            </table>
        </Card>
      </div>
      <div>
      <div id="d2">
        <h3>连接关系</h3>
        <Button type="error">AP</Button>
        <Button type="info">STA</Button>
      </div>
      <div id="container" :style="{height:height,width:width}"></div>

      </div>
      <Table :height="300" :columns="columns1" :data="data1" :stripe=false :width="400" :size="small"></Table>
    </div>
    <Divider><p>统计信息</p></Divider>
      <div id="d1">
      <div id="main" style="width: 300px;height: 400px;float: right;display: inline-block;"></div>
      <div :class="className" :id="id" :style="{height:height,width:width}" ref="srcEchart"></div>
      <div :class="className" :id="id" :style="{height:height,width:width}" ref="desEchart"></div>
      </div>

    </div>

</template>
<style>
.echartLayout {
   margin: auto;
   position: absolute;
   width:30%;
   height:30%;

 }
 #d2{
     display: -webkit-flex;
     display: flex;
     justify-content: space-around;
     height: 10%;
 }
#d1{
    display: -webkit-flex;
    display: flex;
    justify-content: space-around;
    height: 50%;
}
</style>
<script>
import echarts from 'echarts'
//import axios from 'axios'
export default {
  name: "personRelation",
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
      default: '400px'
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
  beforeDestroy() {
    if (!this.chart) {
      return
    }
    this.chart.dispose();
    this.chart = null;
  },
  name: '',
  Ip: '',
  start_date: '',
  stop_date: '',
  //title_ap:'',
  //ap_info:'',
  modal1:'',
  mac :'D4:EE:07:32:01:5A',
  mounted() {
    //this.getdata('D4:EE:07:32:01:5A');
    this.drawDes(),
    this.drawSrc(),
    this.drawPie('main')
    this.initEchart()
  },
  data () {
    return {
      myChart: null,

      modal1: false,
      sites:[
        {name:'D4:EE:07:32:01:5A'},
        {name:'34:23:87:a9:26:9b'},
      ],
      columns1: [
        {
          title: '该AP下活跃的客户端列表',
          align: 'center',
          children:[
            {
              title: 'IP地址',
              key: 'ip',
            },
            {
              title: 'MAC地址',
              key: 'mac'
            },
            {
              title: '操作',
              key: 'action',
              width: '100',
              render: (h,params)=>{
                return h('Button',{
                  props:{
                    type: 'primary',
                    size: 'small'
                  },
                  on:{
                    click: ()=>{
                      this.ip_detail(params.index)
                    }
                  }
                },'详情')
              }
            }
          ]
        }
        ],
      options1: {
        disabledDate (date) {
          return date && date.valueOf() < Date.now() - 86400000;
        }
      },

      charts: '',
      /*
      data1: [],
      opinion:'',
      opinionData:'',
      srcdata_x: '',
      srcdata_y: '',
      desdata_x: '',
      desdata_y: '',
      ap_info: '',
      */
      ap_data: [{
        name: 'xd_stu',
        value: 'D4:EE:07:32:01:5A',
        children: [
          {
            name:'D4:EE:07:32:01:5A',
            value: '192.168.3.1'
          },
          {
            name:'D4:EE:07:32:01:5A'
          },
          {
            name:'D4:EE:07:32:01:5A',
          },
          {
            name:'D4:EE:07:32:01:5A'
          },
          {
            name:'D4:EE:07:32:01:5A'
          },
          {
            name:'D4:EE:07:32:01:5A'
          },
          {
            name:'D4:EE:07:32:01:5A'
          },
        ]
      }],

      ap_info: [
        {
          info_name : 'AP名称(SSID):',
          info_data : 'xd-stu',
        },
        {
          info_name : 'MAC地址:',
          info_data : 'D4:EE:07:32:01:5A',
        },
        {
          info_name : '局域网IP:',
          info_data : '192.168.3.1',
        },
        {
          info_name : '信道:',
          info_data : 11,
        },
        {
          info_name : '信号强度:',
          info_data : '强',
        },
    ],
    aps_data:[{
      name: '周围AP列表',
      children: [
        {
          name:'xd_stu',
          value: 'D4:EE:07:32:01:5A'
        },
        {
          name:'xd_stu',
          value: 'D4:EE:07:32:01:5A'
        },
        {
          name:'xd_stu',
          value: 'D4:EE:07:32:01:5A'
        },
        {
          name:'xd_stu',
          value: 'D4:EE:07:32:01:5A'
        },
        {
          name:'xd_stu',
          value: 'D4:EE:07:32:01:5A'
        },
        {
          name:'xd_stu',
          value: 'D4:EE:07:32:01:5A'
        },
        {
          name:'xd_stu',
          value: 'D4:EE:07:32:01:5A'
        },
        {
          name:'xd_stu',
          value: 'D4:EE:07:32:01:5A'
        },
      ]
    }],

      data1:[
        {ip: '192.168.199.126',mac:'34:23:87:A9:26:9B'},
        {ip: '192.168.3.103',mac:'D4:EE:07:32:01:5A'},
        {ip: '192.168.3.2',mac:'D4:EE:07:32:01:5A'},
        {ip: '192.168.3.3',mac:'D4:EE:07:32:01:5A'},
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
    getdata: function(ap_mac){
      let s = this
      //alert(ap_mac)
      this.$axios.get('getindex',
      {
        params:{
          mac: ap_mac,
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
          s.ap_info = response.data['ap_info'];
          //s.forceUpdate();
          //alert(response.data['ip']);
          s.drawPie('main');
          s.drawSrc();
          s.drawDes();
          s.initEchart();
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
            lineHeight:50,
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
          name: '服务器I流量',
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
            lineHeight:50,
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
            lineHeight:50,
          }
        },
        tooltip: {
          trigger: 'item',
          formatter: '{a}<br/>{b}:{c} ({d}%)'
        },
        legend: {
          orient: 'horizontal',
          x: 'left',
          data:this.opinion,
          bottom:0
        },
        series: [
          {
          name:'访问来源',
          type:'pie',
          radius:['40%','70%'],
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
    choose: function(data,index){
      this.$router.push({
        path: '/parserinfo',
        query:{
          ip : data['ip']
        }
      })
    },
    ip_detail: function(index) {
      //alert(this.Ip);
      this.$router.push({
        path: '/parserinfo',
        query:{
          ip : this.data1[index].ip,
          mac: this.data1[index].mac
        }
      })
    },
    datechange: function(date){
        var month = date.getMonth()+1;
        var year = date.getFullYear();
        var day = date.getDate();
        var d = year+"-"+month+"-"+day;
        return d;
    },
    history: function() {
      //alert(this.start_date.getMonth());
      this.$router.push({
        path: '/history',
        query:{
          ap_info: this.ap_info,
        }
      //
      })
    },
    choose_ap: function(){
      this.apschart()
      this.modal1 = true
    },
    apschart: function(){
      this.myChart = echarts.init(document.getElementById("container1"));
      this.myChart.on("click",function(params){
        if (!(params.name == '周围AP列表')){
              alert(params.name);
        }
      });
      this.myChart.setOption({
        title: {
          text:'周围AP列表',
          left: 10,
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
          formatter: '{b}<br/>{c}'
        },
        series:[{
          type: 'tree',
          data: this.aps_data,
          top: '1%',
          left: '7%',
          bottom: '1%',
          right: '20%',
          symbolSize: 7,
          label: {
            normal: {
              position: 'top',
              verticalAlign: 'middle',
              align: 'left',
              fontSize: 15,
              color: 'red',
            }
          },

          leaves: {
            label: {
              normal: {
                position: 'top',
                verticalAlign: 'middle',
                align: 'middle',
                color: 'blue'
              }
            }
          },
          expandAndCollapse: false,
          animationDuration: 550,
          animationDurationUpdate: 750
            }]
      })
    },
    initEchart: function() {
      this.myChart = echarts.init(document.getElementById("container"));
      this.myChart.setOption({
        //title: {
          //text:'连接关系',
          //subtext: '红色为AP\n蓝色为STA\n绿色为选中的AP',
          //subtextStyle:{
          //  color:"#222",
          //},
          //left: 0,
          //x:'center',
          //textStyle:{
            //color:"#222",
            //fontStyle:"normal",
            //fontWeight:"600",
            //fontFamily:"san-serif",
            //fontSize:16,
          //}
        //},
        //legend: {
          //top:'2%',
          //left:'3%',
          //data:[
          //  {
            //name : '当前AP',
            //color: 'green',
            //icon: 'rectangle'
            //},
            //{
            //name :'当前AP下客户端',
            //color:'black',
            //icon: 'rectangle'
            //}
        //]},
        tooltip: {
          trigger: 'item',
          formatter: '{b}<br/>{c}'
        },
        series:[{
          type: 'tree',
          data: this.ap_data,
          top: '1%',
          left: '7%',
          bottom: '1%',
          right: '20%',
          symbolSize: 7,
          label: {
            normal: {
              position: 'top',
              verticalAlign: 'middle',
              align: 'left',
              fontSize: 15,
              color: 'red',
            }
          },

          leaves: {
            label: {
              normal: {
                position: 'top',
                verticalAlign: 'middle',
                align: 'middle',
                color: 'blue'
              }
            }
          },
          expandAndCollapse: false,
          animationDuration: 550,
          animationDurationUpdate: 750
            }]
      })
    },
    ok: function(){
      alert(1)
    },
    click_ap: function(params){
      if(typeof(params.seriesIndex=='undefined')){
        return;
      }
      if (params.type == 'click') {
        alert(params.name);
      }
    }
  }
}
</script>
