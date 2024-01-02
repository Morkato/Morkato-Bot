import {
  format,
  is_empty,
  strip
} from '../utils/string'

describe("Utilitários: String Testes", () => {
  describe("Formatter", () => {
    test("String Formatter: Equação Simples", () => {
      const text = "$candy é o melhor doce do mundo."
      const textFormatted = format(text, { candy: "Pudim" })
  
      expect(textFormatted).toBe("Pudim é o melhor doce do mundo.")
    })
  
    test("String Formatter: Equação meio Complexa", () => {
      const text = "$candy é o melhor doce do $world."
      const textFormatted = format(text, { candy: "Pudim", world: "mundo" })
  
      expect(textFormatted).toBe("Pudim é o melhor doce do mundo.")
    })
  
    test("String Formatter: Equação Ignorante", () => {
      const text = "\\" + "$candy é o melhor doce do mundo."
      const textFormatted = format(text, { candy: "Pudim" })
  
      expect(textFormatted).toBe("$candy é o melhor doce do mundo.")
    })
  
    test("String Formatter: Equação Ignorante e Complexa", () => {
      const text = "$candy é o melhor doce do \\$world."
      const textFormatted = format(text, { candy: "Pudim" })
  
      expect(textFormatted).toBe("Pudim é o melhor doce do $world.")
    })
  })

  describe("String is Empty", () => {
    test("String is Empty: Somente espaços", () => {
      const text = "                                               "
      const result = is_empty(text)

      expect(result).toBe(true)
    })
    
    test("String is Empty: Espaços e Caracteres", () => {
      const text = "                       c a b                      "
      const result = is_empty(text)

      expect(result).toBe(false)
    })

    test("String is Empty: Espaços e Quebra de Linha", () => {
      const text = "\n\n             \n\n        \n\t           \t       "
      const result = is_empty(text)

      expect(result).toBe(true)
    })

    test("String is Empty: Espaços, Quebra de Linha e Caracteres", () => {
      const text = "\n\n     cd        \n\n    a    \n\t     b      \t       "
      const result = is_empty(text)

      expect(result).toBe(false)
    })
  })

  describe("Text Formatter Strip", () => {
    test("String Formatter Strip: Removendo Espaços no Começo e Final do Texto", () => {
      const text = "  abc     "
      const result = strip(text, { trim: true })

      expect(result).toBe("abc")
    })

    test("String Formatter Strip: Transformando Todas as Letras em Minusculas", () => {
      const text = "ABC"
      const result = strip(text, { case_insensitive: true })

      expect(result).toBe("abc")
    })

    test("String Formatter Strip: Removendo Todos os Acentos das Letras Presente no Texto", () => {
      const text = "ÁBC"
      const result = strip(text, { ignore_accents: true })

      expect(result).toBe("ABC")
    })

    test("String Formatter Strip: Removendo Espaços em Brancos", () => {
      const text = "ABC                       def"
      const result = strip(text, { ignore_empty: true })

      expect(result).toBe("ABC-def")
    })

    test("String Formatter Strip: Complexo - Tudo", () => {
      const text = "      Á           B c                   "
      const result = strip(text, { trim: true, case_insensitive: true, ignore_accents: true, ignore_empty: true })

      expect(result).toBe("a-b-c")
    })
  })
})