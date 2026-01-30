import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  // API rewrites to proxy requests to Kong gateway
  async rewrites() {
    const kongUrl = process.env.KONG_BASE_URL || 'http://localhost:8080'
    return [
      {
        source: '/api/:path*',
        destination: `${kongUrl}/api/:path*`,
      },
    ]
  },
};

export default nextConfig;
