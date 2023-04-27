import { Component, CSSProperties } from "react"
import Image from 'next/image'

export class Embed extends Component<{
  title?: string
  description?: string
  url?: string

  width?: string
  }> {
  render() {
    const style: CSSProperties = {
      width: this.props.width || "auto"
    }
    if(!this.props.url)
      return (
        <div className="embed-tsx" style={style}>
          <div>{this.props.title || 'No title'}</div>
          <span>{this.props.description || 'No description'}</span>
        </div>
      );
    return (
      <div className="embed-tsx" style={style}>
        <h3>{this.props.title || 'No title'}</h3>
        <p>{this.props.description || 'No description'}</p>
        <img src={this.props.url}/>
      </div>
    );
  }
}