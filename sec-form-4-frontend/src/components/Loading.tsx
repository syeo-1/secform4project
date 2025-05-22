import { OrbitProgress } from "react-loading-indicators"

export default function Loading() {
  return (
    <div style={{
      height: '100%',
      width: '100%',
      alignItems: 'center',
      display: 'flex',
      justifyContent: 'center'
    }}>
      <OrbitProgress color="white" size="large" text="" textColor=""
      />
    </div>
  )
}