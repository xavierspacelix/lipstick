import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  async rewrites() {
    return [
      {
        source: "/api/v1/images/:path*",
        destination: `${process.env.NEXT_PUBLIC_API_URL}/api/v1/images/:path*`,
      },
    ];
  },
};

export default nextConfig;