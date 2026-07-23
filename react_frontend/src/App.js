import { useState, useEffect } from 'react';
import axios from 'axios';
import { Layout, Menu, Button, Input, Card, message } from 'antd';
import EChartsReact from 'echarts-for-react';
import { BrowserRouter, Routes, Route, Navigate, useNavigate } from 'react-router-dom';
import "antd/dist/reset.css";

const { Sider, Content } = Layout;
axios.defaults.withCredentials = true;

// 登录页面
function Login() {
  const navigate = useNavigate();
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");

  const doLogin = async () => {
    const res = await axios.post("http://127.0.0.1:5000/api/login", { username, password });
    if(res.data.code === 200){
      message.success("登录成功");
      navigate("/dashboard");
    }else{
      message.error(res.data.msg);
    }
  };

  return (
    <div style={{width:400, margin:"100px auto"}}>
      <Card title="用户登录">
        <Input placeholder="用户名" value={username} onChange={e=>setUsername(e.target.value)} style={{marginBottom:10}}/>
        <Input type="password" placeholder="密码" value={password} onChange={e=>setPassword(e.target.value)} style={{marginBottom:10}}/>
        <Button block type="primary" onClick={doLogin}>登录</Button>
        <Button block onClick={()=>navigate("/register")} style={{marginTop:8}}>前往注册</Button>
      </Card>
    </div>
  )
}

// 注册页面
function Register() {
  const navigate = useNavigate();
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");

  const doRegister = async () => {
    const res = await axios.post("http://127.0.0.1:5000/api/register", { username, password });
    if(res.data.code === 200){
      message.success("注册成功，请登录");
      navigate("/login");
    }else{
      message.error(res.data.msg);
    }
  };

  return (
    <div style={{width:400, margin:"100px auto"}}>
      <Card title="用户注册">
        <Input placeholder="用户名" value={username} onChange={e=>setUsername(e.target.value)} style={{marginBottom:10}}/>
        <Input type="password" placeholder="密码" value={password} onChange={e=>setPassword(e.target.value)} style={{marginBottom:10}}/>
        <Button block type="primary" onClick={doRegister}>注册</Button>
        <Button block onClick={()=>navigate("/login")} style={{marginTop:8}}>返回登录</Button>
      </Card>
    </div>
  )
}

// 图表主页（登录后）
function Dashboard() {
  const navigate = useNavigate();
  const [activeKey, setActiveKey] = useState("year");
  const [chartData, setChartData] = useState([]);

  const logout = async () => {
    await axios.post("http://127.0.0.1:5000/api/logout");
    navigate("/login");
  };

  useEffect(()=>{
    const fetchData = async () => {
      let url = "";
      switch(activeKey) {
        case "year": url = "http://127.0.0.1:5000/api/chart/year_count"; break;
        case "region": url = "http://127.0.0.1:5000/api/chart/region_count"; break;
        case "type": url = "http://127.0.0.1:5000/api/chart/type_count"; break;
        case "score": url = "http://127.0.0.1:5000/api/chart/score_vote"; break;
        default: return;
      }
      const res = await axios.get(url);
      setChartData(res.data.data);
    };
    fetchData();
  },[activeKey])

  const getOption = () => {
    switch(activeKey) {
      case "year":
        return {title:{text:"各年份电影数量分布"},xAxis:{type:"category", data:chartData.map(i=>i.year)},yAxis:{type:"value"},series:[{type:"bar", data:chartData.map(i=>i.count)}]}
      case "region":
        return {title:{text:"各制片地区电影数量"},xAxis:{type:"category", data:chartData.map(i=>i.name)},yAxis:{type:"value"},series:[{type:"bar", data:chartData.map(i=>i.value)}]}
      case "type":
        return {title:{text:"影片类型占比"},series:[{type:"pie", radius:"50%", data:chartData}]}
      case "score":
        return {title:{text:"评分-评价人数热度散点图"},xAxis:{type:"value", name:"评分"},yAxis:{type:"value", name:"评价人数"},series:[{type:"scatter", data:chartData.map(i=>[i.score,i.vote,i.name])}]}
      default: return {}
    }
  }

  return (
    <Layout style={{minHeight:"100vh"}}>
      <Sider width={200}>
        <Menu mode="vertical" selectedKeys={[activeKey]} onClick={({key})=>setActiveKey(key)} style={{height:"90%"}}>
          <Menu.Item key="year">年份统计柱状图</Menu.Item>
          <Menu.Item key="region">地区统计柱状图</Menu.Item>
          <Menu.Item key="type">影片类型饼图</Menu.Item>
          <Menu.Item key="score">评分热度散点图</Menu.Item>
        </Menu>
        <Button danger block onClick={logout} style={{margin:10}}>退出登录</Button>
      </Sider>
      <Content style={{padding:30}}>
        <EChartsReact option={getOption()} style={{width:"100%", height:"600px"}}/>
      </Content>
    </Layout>
  )
}

// 路由权限守卫
function RequireAuth() {
  const [auth, setAuth] = useState(null);
  const navigate = useNavigate();
  useEffect(()=>{
    axios.get("http://127.0.0.1:5000/api/check_login").then(res=>{
      if(res.data.isLogin) setAuth(true);
      else navigate("/login");
    })
  },[])
  if(auth === null) return <div>加载中...</div>
  return <Dashboard/>
}

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Navigate to="/login"/>}/>
        <Route path="/login" element={<Login/>}/>
        <Route path="/register" element={<Register/>}/>
        <Route path="/dashboard" element={<RequireAuth/>}/>
      </Routes>
    </BrowserRouter>
  );
}

export default App;