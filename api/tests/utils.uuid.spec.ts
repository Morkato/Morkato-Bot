import { uuid, created_at } from '../utils/uuid'

describe("Utilitários: UUID - Snowflake ID", () => {
  describe("UUID: Geração de IDS", () => {
    test("UUID: TimeZone", () => {
      const instant = Date.now()
      const id = uuid(instant)

      expect(created_at(id)).toBe(instant)
    })
  })
})