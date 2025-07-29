/** @type {import('next').NextConfig} */
const nextConfig = {
  eslint: {
    ignoreDuringBuilds: true,
  },
  typescript: {
    ignoreBuildErrors: true,
  },
  images: {
    unoptimized: true,
  },
  async rewrites() {
    const backendApiUrl = process.env.NEXT_PUBLIC_API_URL;

    if (!backendApiUrl) {
      console.warn(
        "Warning: NEXT_PUBLIC_API_URL is not set. API rewrites might not work as expected."
      );
      // Fallback or prevent rewrites if the URL isn't set
      return [];
    }


    return [
      {
        source: '/api/:path*',
        destination: `${backendApiUrl}/api/:path*`,
      },
    ]
    },
    
}

export default nextConfig
