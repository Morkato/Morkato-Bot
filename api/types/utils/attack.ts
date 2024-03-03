import type { Attack } from 'type:models/attack'
import type { Art } from 'type:models/art'

export type IsUniqueAttackByNameParameter = Partial<Pick<Attack, 'id'>> & Pick<Attack, 'name' | 'parent_id'> & { attacks: Attack[], art_id: string, is_fight_style: boolean }