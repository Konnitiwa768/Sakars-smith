
system.runInterval(() => {
  for (const player of world.getPlayers()) {
    const raycastResult = player.raycast(10, 0, false); // 10ブロック先まで視線
    if (raycastResult && raycastResult.entity) {
      const entity = raycastResult.entity;
      const hp = entity.getComponent("health")?.current ?? 0;
      player.runCommand(`tellraw @s {"rawtext":[{"text":"視線先の${entity.id}のHP: ${hp}"}]}`);
    }
  }
}, 20); // 20 tick = 1秒ごと
