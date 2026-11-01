/**
 * Maps our provisioned default stage names (English, from backend seed)
 * to i18n keys. User-created stages don't match and stay as-is.
 */
const STAGE_KEY_MAP: Record<string, string> = {
    qualified: "deals.stages.qualified",
    proposal: "deals.stages.proposal",
    negotiation: "deals.stages.negotiation",
    won: "deals.stages.won",
    lost: "deals.stages.lost",
}

export function translateStage(
    name: string,
    t: (key: string) => string,
): string {
    const key = STAGE_KEY_MAP[name.trim().toLowerCase()]
    if (!key) return name
    const translated = t(key)
    // If key missing in this locale, vue-i18n returns the key itself
    return translated === key ? name : translated
}