import type { Attack } from 'type:models/attack'

export type IsUniqueAttackByNameParameter = Partial<Pick<Attack, 'id'>> & Pick<Attack, 'name' | 'art_id' | 'item_id' | 'parent_id'> & { attacks: Attack[] }