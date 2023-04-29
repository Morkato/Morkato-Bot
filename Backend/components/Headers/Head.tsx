import NextHead from 'next/head'
import { Component, ReactNode } from "react"
import Script from 'next/script'
import Link from 'next/link'

export class Head extends Component<{
  title?: string
  description?: string
  type?: string
  scripts?: { src?: string, crossorigin?: "" | "anonymous" | "use-credentials", integrity?: string }[]
  links?: { rel?: string, href?: string, crossorigin?: "" | "anonymous" | "use-credentials", integrity?: string }[]
  methods?: (() => ReactNode)[]
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

        {(this.props.scripts || []).map(e => <Script src={e.src} crossOrigin={e.crossorigin} integrity={e.integrity} />)}

        {(this.props.links || []).map(e => <link rel={e.rel} href={e.href} crossOrigin={e.crossorigin} integrity={e.integrity} />)}

        {(this.props.methods || []).map(comp => comp())}
      </NextHead>
    )
  }
}