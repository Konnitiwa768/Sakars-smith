import { world, system, ItemStack, ItemTypes } from "@minecraft/server";

// エンチャント定義
const ENCHANTS = [
    {
        key: "超加速",
        display: "§b超加速",
        ability: "移動速度大幅アップ（攻撃時にSpeed付与）",
        material: "minecraft:diamond",
        perLevel: 3,
        max: 6,
        color: "§b",
        effect: "speed"
    },
    {
        key: "無限耐久",
        display: "§e無限耐久",
        ability: "耐久値消費なし（常時Unbreakable効果）",
        material: "minecraft:netherite_ingot",
        perLevel: 3,
        max: 6,
        color: "§e",
        effect: "unbreakable"
    },
    {
        key: "治癒力",
        display: "§a治癒力",
        ability: "HP自動回復（常時Regeneration付与）",
        material: "minecraft:golden_apple",
        perLevel: 1,
        max: 3,
        color: "§a",
        effect: "regen"
    },
    {
        key: "炎上付与",
        display: "§6炎上付与",
        ability: "攻撃時に炎上（Fire付与）",
        material: "minecraft:blaze_powder",
        perLevel: 2,
        max: 6,
        color: "§6",
        effect: "fire_aspect"
    },
    {
        key: "雷撃",
        display: "§9雷撃",
        ability: "攻撃時に雷（Lightning召喚）",
        material: "minecraft:trident",
        perLevel: 1,
        max: 2,
        color: "§9",
        effect: "thunder"
    },
    {
        key: "爆破強化",
        display: "§c爆破強化",
        ability: "攻撃時に爆発（範囲拡大）",
        material: "minecraft:gunpowder",
        perLevel: 2,
        max: 6,
        color: "§c",
        effect: "explosion"
    },
    {
        key: "水中呼吸",
        display: "§3水中呼吸",
        ability: "水中でも呼吸可能（常時Water Breathing）",
        material: "minecraft:heart_of_the_sea",
        perLevel: 1,
        max: 1,
        color: "§3",
        effect: "water_breath"
    },
    {
        key: "瞬間移動",
        display: "§d瞬間移動",
        ability: "右クリックで前方にワープ",
        material: "minecraft:ender_pearl",
        perLevel: 2,
        max: 4,
        color: "§d",
        effect: "teleport"
    },
    {
        key: "跳躍力",
        display: "§a跳躍力",
        ability: "攻撃時にJump Boost付与",
        material: "minecraft:slime_ball",
        perLevel: 3,
        max: 6,
        color: "§a",
        effect: "jump"
    },
    {
        key: "透明化",
        display: "§7透明化",
        ability: "攻撃時に透明化付与",
        material: "minecraft:glass",
        perLevel: 4,
        max: 3,
        color: "§7",
        effect: "invisible"
    }
];

// lore付き剣作成
function createEnchantedSword(enchant, level) {
    const sword = new ItemStack(ItemTypes.get("minecraft:iron_sword"), 1);
    sword.setLore([
        `${enchant.color}${enchant.display} Lv.${level}`,
        `§7能力: ${enchant.ability}`
    ]);
    sword.setDynamicProperty("custom_enchant", JSON.stringify({
        key: enchant.key,
        level: level,
        effect: enchant.effect
    }));
    // 無限耐久の場合はUnbreakableフラグを付ける
    if (enchant.effect === "unbreakable") {
        sword.setComponent("minecraft:unbreakable", { value: true });
    }
    return sword;
}

// 素材と数からエンチャント種類とLvを決定
function judgeEnchant(materialId, count) {
    const enchant = ENCHANTS.find(e => e.material === materialId);
    if (!enchant) return null;
    let level = Math.floor(count / enchant.perLevel);
    if (level < 1) level = 1;
    if (level > enchant.max) level = enchant.max;
    return { enchant, level };
}

// 剣作成イベント: 素材を地面に使った時
world.afterEvents.itemUseOn.subscribe(event => {
    const player = event.source;
    if (!player) return;
    const item = event.item;
    if (!item) return;

    // エンチャント判定
    const res = judgeEnchant(item.typeId, item.amount);
    if (!res) return;

    // 必要素材数だけ消費
    if (player.hasComponent("inventory")) {
        const inv = player.getComponent("inventory").container;
        let remain = res.enchant.perLevel * res.level;
        for (let i = 0; i < inv.size; i++) {
            const invItem = inv.getItem(i);
            if (invItem && invItem.typeId === item.typeId) {
                if (invItem.amount > remain) {
                    invItem.amount -= remain;
                    inv.setItem(i, invItem);
                    remain = 0;
                    break;
                } else {
                    remain -= invItem.amount;
                    inv.setItem(i, undefined);
                }
            }
        }
    }

    // lore・能力情報付き剣を出現
    const sword = createEnchantedSword(res.enchant, res.level);
    world.getDimension("overworld").spawnItem(sword, player.location);
    player.sendMessage(`${res.enchant.color}${res.enchant.display}§r Lv.${res.level}の剣（§7${res.enchant.ability}§r）を手に入れた！`);
});

// 能力発動（全てswitchで省略なし！）

// 攻撃時（entityHurt）で発動する能力
world.afterEvents.entityHurt.subscribe(event => {
    const attacker = event.damageSource.damagingEntity;
    if (!attacker?.hasComponent("inventory")) return;
    const heldItem = attacker.getComponent("inventory").container.getItem(attacker.selectedSlot);
    if (!heldItem || !heldItem.getDynamicProperty("custom_enchant")) return;

    const enchantData = JSON.parse(heldItem.getDynamicProperty("custom_enchant"));
    switch (enchantData.effect) {
        case "speed":
            attacker.addEffect("speed", 40, enchantData.level, false);
            break;
        case "fire_aspect":
            if (event.hurtEntity) event.hurtEntity.setOnFire(40 * enchantData.level);
            break;
        case "thunder":
            if (event.hurtEntity) {
                world.getDimension("overworld").spawnEntity("minecraft:lightning_bolt", event.hurtEntity.location);
            }
            break;
        case "explosion":
            if (event.hurtEntity) {
                world.getDimension("overworld").createExplosion(
                    event.hurtEntity.location,
                    2 + enchantData.level * 0.5,
                    { breaksBlocks: false }
                );
            }
            break;
        case "jump":
            attacker.addEffect("jump_boost", 40, enchantData.level, false);
            break;
        case "invisible":
            attacker.addEffect("invisibility", 60, enchantData.level, false);
            break;
    }
});

// プレイヤー常時発動
system.runInterval(() => {
    for (const player of world.getPlayers()) {
        const item = player.getComponent("inventory").container.getItem(player.selectedSlot);
        if (!item || !item.getDynamicProperty("custom_enchant")) continue;
        const enchantData = JSON.parse(item.getDynamicProperty("custom_enchant"));
        switch (enchantData.effect) {
            case "regen":
                player.addEffect("regeneration", 40, enchantData.level, false);
                break;
            case "unbreakable":
                player.addEffect("resistance", 40, 2, false); // 擬似的に無限耐久としてResistance
                break;
            case "water_breath":
                player.addEffect("water_breathing", 40, enchantData.level, false);
                break;
        }
    }
}, 40); // 2秒ごと

// 瞬間移動（右クリック時）
world.afterEvents.itemUse.subscribe(event => {
    const player = event.source;
    const item = event.item;
    if (!item || !item.getDynamicProperty("custom_enchant")) return;
    const enchantData = JSON.parse(item.getDynamicProperty("custom_enchant"));
    if (enchantData.effect === "teleport") {
        // プレイヤーの向いてる方向に3ブロック×Lv先へテレポート
        const dir = player.getViewDirection();
        const newPos = {
            x: player.location.x + dir.x * 3 * enchantData.level,
            y: player.location.y,
            z: player.location.z + dir.z * 3 * enchantData.level
        };
        player.teleport(newPos, { facingLocation: undefined });
        player.sendMessage("§d瞬間移動！");
    }
});
