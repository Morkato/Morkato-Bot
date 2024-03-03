export function formatDecimalsNumber(num: number, decimals?: number): string {
  decimals = decimals ?? 1
  const numText = num.toString()

  if (numText.length < decimals) {
    return "0".repeat(decimals - numText.length) + num.toString();
  }

  return numText;
}

const directivesDateFormat: Partial<Record<string, (date: Date) => string>> = {
  d(date: Date): string {
    return formatDecimalsNumber(date.getDate(), 2);
  },
  m(date: Date): string {
    return formatDecimalsNumber(date.getMonth(), 2);
  },
  y(date: Date): string {
    return formatDecimalsNumber(date.getFullYear() % 1000, 2);
  },
  Y(date: Date): string {
    return formatDecimalsNumber(date.getFullYear(), 2);
  },
  H(date: Date): string {
    return formatDecimalsNumber(date.getHours(), 2);
  },
  h(date: Date): string {
    return formatDecimalsNumber(Math.abs((date.getHours() - 12) * -1), 2);
  },
  M(date: Date): string {
    return formatDecimalsNumber(date.getMinutes(), 2);
  },
  S(date: Date): string {
    return formatDecimalsNumber(date.getSeconds(), 2);
  }
}

export class StringView {
  static formatLoggerSintaxe(text: string, args: string[], kwargs: Partial<Record<string, string>>): string {
    if (!args && !kwargs) {
      return text;
    }

    const view = new StringView(text)
    
    let finalText = ""
    let current = view.current()
    let currentArgIndex = 0

    while (!view.eof() && current !== null) {
      if (current === '%') {
        view.next()
        
        const key = view.word()

        if (['s', 'c'].includes(key)) {
          const currentArgValue = args[currentArgIndex] ?? "NaN"
          currentArgIndex += 1

          finalText += currentArgValue
        } else if (/[0-9]+/.test(key)) {
          finalText += args[Number(key)] ?? "%" + key
        } else {
          const value = kwargs[key] ?? "%" + key

          finalText += value
        }

        current = view.current()
        continue;
      }
      
      finalText += current
      current = view.next()
    }

    return finalText;
  }

  static timeFormat(date: Date, formatter: string): string {
    const view = new StringView(formatter)
    
    let current = view.current()
    let finalText = ""

    while (!view.eof() && current !== null) {
      if (current === '%') {
        const next_char = view.next()
        
        if (next_char === null) {
          break;
        }

        const directive = directivesDateFormat[next_char]

        if (directive) {
          finalText += directive(date)
          current = view.next()
          continue;
        } else {
          view.undo()
        }
      } else if (current === '\\') {
        const next_char = view.next()

        if (next_char === null) {
          break;
        } else if (['\\', '%'].includes(next_char)) {
          finalText += next_char
          current = view.next()
          continue;
        }
      }

      finalText += current
      current = view.next()
    }

    return finalText;
  }

  private idx: number = 0
  private prev: number = 0
  private end: number
  
  constructor(
    private readonly buffer: string
  ) {
    this.end = buffer.length
  }

  eof() {
    return this.idx >= this.end;
  }

  current(): string | null {
    return this.buffer[this.idx] ?? null;
  }

  next(): string | null {
    const result = this.buffer[this.idx + 1] ?? null

    this.prev = this.idx
    this.idx += 1

    return result;
  }

  undo() {
    this.idx = this.prev
  }

  word(): string {
    this.prev = this.idx
    
    while (!this.eof() && /[a-z0-9]/i.test(this.buffer[this.idx])) {
      this.idx += 1
    }

    return this.buffer.slice(this.prev, this.idx);
  }

  skip(regex: RegExp): void {
    this.prev = this.idx

    while (!this.eof() && regex.test(this.buffer[this.idx])) {
      this.idx += 1
    }
  }
}