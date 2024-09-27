import { useState } from 'react'
import './App.css'
import GameBoard from './components/boardComponent'
import Board from './components/board'

function App() {
  const [count, setCount] = useState(0)

  return (
    <>
     <h1>welcome to 9mens morris game</h1>
     <GameBoard />
     
    </>
  )
}

export default App
