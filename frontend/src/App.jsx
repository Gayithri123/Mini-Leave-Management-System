import React, { useEffect, useState } from 'react'
import './App.css'

const API = import.meta.env.VITE_API_BASE || 'http://localhost:8000'

function AddEmployee(){
  const [form,setForm]=useState({id:'',name:'',email:'',department:'',joining_date:''})

  useEffect(()=>{
    (async()=>{
      const r=await fetch(${API}/employees/next-id)
      const j=await r.json()
      setForm(f=>({...f,id:j.next_id}))
    })()
  },[])

  const submit=async(e)=>{
    e.preventDefault()
    const r=await fetch(${API}/employees,{
      method:'POST',
      headers:{'Content-Type':'application/json'},
      body:JSON.stringify(form)
    })
    const j=await r.json()
    alert(j.message || j.detail || 'done')
    if(j.employee?.id) setForm({...form,id:j.employee.id})
  }
  return (
    <form onSubmit={submit} className="form">
      <h3>Add Employee</h3>
      <input placeholder='id (auto)' value={form.id} readOnly />
      <input placeholder='name' value={form.name} onChange={e=>setForm({...form,name:e.target.value})}/>
      <input placeholder='email' value={form.email} onChange={e=>setForm({...form,email:e.target.value})}/>
      <input placeholder='department' value={form.department} onChange={e=>setForm({...form,department:e.target.value})}/>
      <input placeholder='joining_date (YYYY-MM-DD)' value={form.joining_date} onChange={e=>setForm({...form,joining_date:e.target.value})}/>
      <button>Add</button>
    </form>
  )
}

function ApplyLeave(){
  const [form,setForm]=useState({id:'',employee_id:'',start_date:'',end_date:'',reason:''})

  useEffect(()=>{
    (async()=>{
      const r=await fetch(${API}/leaves/next-id)
      const j=await r.json()
      setForm(f=>({...f,id:j.next_id}))
    })()
  },[])

  const submit=async(e)=>{
    e.preventDefault()
    const r=await fetch(${API}/leaves/apply,{
      method:'POST',
      headers:{'Content-Type':'application/json'},
      body:JSON.stringify(form)
    })
    const j=await r.json()
    alert(j.message || j.detail || 'done')
    if(j.leave?.id) setForm({...form,id:j.leave.id})
  }
  return (
    <form onSubmit={submit} className="form">
      <h3>Apply Leave</h3>
      <input placeholder='leave id (auto)' value={form.id} readOnly />
      <input placeholder='employee id' value={form.employee_id} onChange={e=>setForm({...form,employee_id:e.target.value})}/>
      <input placeholder='start_date (YYYY-MM-DD)' value={form.start_date} onChange={e=>setForm({...form,start_date:e.target.value})}/>
      <input placeholder='end_date (YYYY-MM-DD)' value={form.end_date} onChange={e=>setForm({...form,end_date:e.target.value})}/>
      <input placeholder='reason' value={form.reason} onChange={e=>setForm({...form,reason:e.target.value})}/>
      <button>Apply</button>
    </form>
  )
}

function Approvals(){
  const [pending,setPending]=useState([])
  const [id,setId]=useState('')
  const load=async()=>{
    const r=await fetch(${API}/leaves/pending)
    const j=await r.json()
    setPending(j.pending||[])
  }
  useEffect(()=>{load()},[])
  const approve=async()=>{
    const r=await fetch(${API}/leaves/approve,{
      method:'POST',
      headers:{'Content-Type':'application/json'},
      body:JSON.stringify({id})
    })
    const j=await r.json()
    alert(j.message || j.detail || 'done'); load()
  }
  const reject=async()=>{
    const reason=prompt('Reason?')||''
    const r=await fetch(${API}/leaves/reject,{
      method:'POST',
      headers:{'Content-Type':'application/json'},
      body:JSON.stringify({id,reason})
    })
    const j=await r.json()
    alert(j.message || j.detail || 'done'); load()
  }
  return (
    <div className="section">
      <h3>Pending Approvals</h3>
      <button onClick={load}>Refresh</button>
      <ul>
        {pending.map(p=>(<li key={p.id}>{p.id} • Emp:{p.employee_id} • {p.start_date}→{p.end_date} • {p.days}d</li>))}
      </ul>
      <input placeholder='leave id' value={id} onChange={e=>setId(e.target.value)}/>
      <button onClick={approve}>Approve</button>
      <button onClick={reject}>Reject</button>
    </div>
  )
}

function Balance(){
  const [emp,setEmp]=useState('')
  const [bal,setBal]=useState(null)
  const fetchBal=async()=>{
    const r=await fetch(${API}/employees/${emp}/balance)
    const j=await r.json()
    setBal(j.balance ?? j.detail)
  }
  return (
    <div className="section">
      <h3>Check Balance</h3>
      <input placeholder='employee id' value={emp} onChange={e=>setEmp(e.target.value)}/>
      <button onClick={fetchBal}>Fetch</button>
      {bal!==null && <div>Balance: {bal}</div>}
    </div>
  )
}

export default function App(){
  const [tab,setTab]=useState('employees')
  return (
    <div className="app">
      <h2>Mini Leave Management</h2>
      <nav>
        <button onClick={()=>setTab('employees')}>Add Employee</button>
        <button onClick={()=>setTab('apply')}>Apply Leave</button>
        <button onClick={()=>setTab('approvals')}>Approvals</button>
        <button onClick={()=>setTab('balance')}>Balance</button>
      </nav>
      {tab==='employees' && <AddEmployee/>}
      {tab==='apply' && <ApplyLeave/>}
      {tab==='approvals' && <Approvals/>}
      {tab==='balance' && <Balance/>}
    </div>
  )
}