import NextHead from 'next/head'
import { Component } from "react"

export class Head extends Component<{
  title?: string
  description?: string
  type?: string
  scripts?: string[]
  styles?: string[]
  stylesString?: string[]
}> {
  render() {
    const [ title, description, type ] = [ this.props.title || "Morkato Bot", this.props.description || "Apenas um simples bot.", this.props.type || "website" ]
    
    return (
      <NextHead>
        <title>{title}</title>
        <meta name="title" content={title} key="title" />
        <meta name="description" content={description} key="description" />
        <meta name="robots" content="index follow" key="robots" />
        
        <meta property="og:site_name" content="Morkato Bot" />
        <meta property="og:type" content={type} />
        <meta property="og:title" content={title} key="og:title" />
        <meta property="og:description" content={description} key="og:description" />

        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <meta name="mobile-web-app-capable" content="yes" />
        <meta name="apple-mobile-web-app-capable" content="yes" />

        {(this.props.scripts || []).map(e => <script src={e}></script>)}

        {(this.props.styles || []).map(e => <link rel="stylesheet" href={e}></link>)}

        {(this.props.stylesString || []).map(e => <style>{e}</style>)}
      </NextHead>
    )
  }
}