import dotenv from 'dotenv';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

// 加载环境变量
dotenv.config({ path: path.join(__dirname, '.env') });

console.log('=== 环境变量测试 ===');
console.log('DOUYIN_CLIENT_KEY:', process.env.DOUYIN_CLIENT_KEY);
console.log('DOUYIN_CLIENT_SECRET:', process.env.DOUYIN_CLIENT_SECRET);
console.log('DOUYIN_REDIRECT_URI:', process.env.DOUYIN_REDIRECT_URI);
console.log('PORT:', process.env.PORT);

// 验证配置是否完整
const hasConfig = process.env.DOUYIN_CLIENT_KEY && process.env.DOUYIN_CLIENT_SECRET;
console.log('\n配置完整性:', hasConfig ? '完整 ✅' : '不完整 ❌');