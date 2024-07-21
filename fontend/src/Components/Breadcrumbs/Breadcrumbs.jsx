import React from 'react'
import './Breadcrumbs.css'

import arrow_icon from '../Assets/breadcrum_arrow.png'

const Breadcrumbs = (props) => {
  const { product } = props
  return (
    <div className="breadcrumb">
      Home <img src={arrow_icon} alt="Arrow" /> Shop{' '}
      <img src={arrow_icon} alt="Arrow" />
      {product.category}
      <img src={arrow_icon} alt="Arrow" />
      {product.name}
    </div>
  )
}

export default Breadcrumbs
