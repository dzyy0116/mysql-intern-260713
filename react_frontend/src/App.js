import { useState } from 'react';
import axios from 'axios';

function App() {
  // 三个输入框绑定状态
  const [input1, setInput1] = useState('');
  const [input2, setInput2] = useState('');
  const [input3, setInput3] = useState('');
  // 后端返回结果展示
  const [resMsg, setResMsg] = useState('');

  // 按钮1：GET请求，传input1作为url参数
  const handleGetReq = async () => {
    try {
      const res = await axios.get(`http://127.0.0.1:5000/api/get_demo`, {
        params: {
          text: input1
        }
      });
      setResMsg(res.data.msg);
    } catch (err) {
      setResMsg("请求失败，请检查后端服务是否启动");
    }
  };

  // 按钮2：POST请求，input2放body，input3放url param
  const handlePostReq = async () => {
    try {
      const res = await axios.post(
        `http://127.0.0.1:5000/api/post_demo?param_text=${input3}`,
        {
          body_text: input2
        }
      );
      setResMsg(res.data.msg);
    } catch (err) {
      setResMsg("请求失败，请检查后端服务是否启动");
    }
  };

  return (
    <div style={{ padding: "40px", width: "600px", margin: "0 auto" }}>
      <h2>第四周前后端联调Demo</h2>
      <div style={{ margin: "16px 0" }}>
        <p>输入框1（GET参数）：</p>
        <input
          value={input1}
          onChange={(e) => setInput1(e.target.value)}
          style={{ width: "100%", padding: "8px" }}
          placeholder="输入内容，点击下方GET按钮发送"
        />
        <button onClick={handleGetReq} style={{ marginTop: "8px", padding: "6px 16px" }}>
          GET发送（任务2）
        </button>
      </div>

      <div style={{ margin: "16px 0" }}>
        <p>输入框2（POST-body参数）：</p>
        <input
          value={input2}
          onChange={(e) => setInput2(e.target.value)}
          style={{ width: "100%", padding: "8px" }}
          placeholder="POST请求body内容"
        />
      </div>

      <div style={{ margin: "16px 0" }}>
        <p>输入框3（POST-url参数）：</p>
        <input
          value={input3}
          onChange={(e) => setInput3(e.target.value)}
          style={{ width: "100%", padding: "8px" }}
          placeholder="POST请求url拼接参数"
        />
        <button onClick={handlePostReq} style={{ marginTop: "8px", padding: "6px 16px" }}>
          POST发送（任务3）
        </button>
      </div>

      <div style={{ marginTop: "30px", border: "1px solid #ccc", padding: "12px" }}>
        <h4>后端返回结果：</h4>
        <p>{resMsg}</p>
      </div>
    </div>
  );
}

export default App;