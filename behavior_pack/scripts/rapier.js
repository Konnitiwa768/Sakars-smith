import { world } from "@minecraft/server";

// レイピアで攻撃時の特殊処理
world.afterEvents.entityHit.subscribe(ev => {
    const { damagingEntity, hitEntity } = ev;
    if (!damagingEntity || !hitEntity) return;
    // レイピア判定（アイテムIDに"rapier"を含む場合）
    const item = damagingEntity.getComponent("minecraft:equippable")?.getEquipment("mainhand");
    if (item && item.typeId?.includes("rapier")) {
        // 無敵時間をリセット（Bedrock APIでは resetLastHurtByPlayer 等を利用）
        if (typeof hitEntity.resetLastHurtByPlayer === "function") {
            hitEntity.resetLastHurtByPlayer();
        }
        // 防御力を取得（armor値はgetComponent("minecraft:armor")などで取得可）
        const armor = hitEntity.getComponent("minecraft:armor")?.protection || 0;
        // 追加ダメージ（例：防御力の0.5倍）
        if (typeof hitEntity.applyDamage === "function" && armor > 0) {
            hitEntity.applyDamage(armor * 0.5, { cause: "custom", damagingEntity });
        }
    }
});
