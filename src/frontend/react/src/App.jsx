import { useEffect, useState } from "react"
import axios from "axios"

function App() {

  const [message, setMessage] = useState("Loading...")

  useEffect(() => {

    axios.get("http://127.0.0.1:8000/")
      .then(res => {
        setMessage(res.data.message)
      })

  }, [])

  return (
    <h1>{message}</h1>
  )
}

export default App