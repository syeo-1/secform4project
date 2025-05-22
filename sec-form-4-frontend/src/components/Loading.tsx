import { OrbitProgress } from "react-loading-indicators"

export default function Loading() {
  return (
    <>
      <OrbitProgress style={{
        alignItems: 'center',
        justifyContent: 'center',
      }}
        color="white" size="medium" text="" textColor=""
      />
    </>
  )
}