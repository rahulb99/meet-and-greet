import { Scene } from 'phaser';

export class Preloader extends Scene
{
    constructor ()
    {
        super('Preloader');
    }

    preload ()
    {
        this.load.setPath('assets');

        // General assets
        this.load.image('background', 'talking_celebs.png');

        // Tilesets
        this.load.image("tuxmon-tiles", "tilesets/tuxmon-sample-32px-extruded.png");
        this.load.image("greece-tiles", "tilesets/ancient_greece_tileset.png");
        this.load.image("plant-tiles", "tilesets/plant.png");

        // Tilemap
        this.load.tilemapTiledJSON("map", "tilemaps/philoagents-town.json");

        // Character assets
        this.load.atlas("sophia", "characters/sophia/atlas.png", "characters/sophia/atlas.json");
        this.load.atlas("trump", "characters/trump/atlas.png", "characters/trump/atlas.json"); 
        this.load.atlas("srk", "characters/srk/atlas.png", "characters/srk/atlas.json"); 
        this.load.atlas("modi", "characters/modi/atlas.png", "characters/modi/atlas.json"); 
        this.load.atlas("sydney_sweeney", "characters/sydney/atlas.png", "characters/sydney/atlas.json"); 
        this.load.atlas("cr7", "characters/cr7/atlas.png", "characters/cr7/atlas.json"); 
        this.load.atlas("bill_gates", "characters/bill_gates/atlas.png", "characters/bill_gates/atlas.json"); 
        this.load.atlas("mr_beast", "characters/mr_beast/atlas.png", "characters/mr_beast/atlas.json"); 
    }

    create ()
    {
        this.scene.start('MainMenu');
    }
}
