require('dotenv').config();


/**@type { import('next').NextConfig } */
module.exports = {
  async rewrites() {
    return [
      {
        source: '/guilds/:guild_id/:path*',
        destination: '/app/guilds/[guild_id]/route',
      },
    ];
  }
}
