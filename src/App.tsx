import { useState, useRef, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Send, Settings, User, MessageSquare, Info, Lock, Loader2 } from 'lucide-react';
import { cn } from './lib/utils';

interface Message {
  id: string;
  role: 'user' | 'assistant';
  content: string;
}

// Configuración de Hugging Face
const HF_API_KEY = "TU_TOKEN_AQUI"; // El usuario lo llenará después
const HF_MODEL = "mistralai/Mistral-7B-Instruct-v0.2"; // Modelo por defecto

async function queryHuggingFace(text: string) {
  try {
    const response = await fetch(
      `https://api-inference.huggingface.co/models/${HF_MODEL}`,
      {
        headers: { Authorization: `Bearer ${HF_API_KEY}` },
        method: "POST",
        body: JSON.stringify({ inputs: text }),
      }
    );
    const result = await response.json();
    return result[0]?.generated_text || "Lo siento, no pude obtener una respuesta.";
  } catch (error) {
    console.error("HF Error:", error);
    return "Error al conectar con Hugging Face. Por favor, verifica tu configuración.";
  }
}

export default function App() {
  const [messages, setMessages] = useState<Message[]>([
    { id: '1', role: 'assistant', content: '¡Hola! Soy Carl AI. He sido diseñado con una interfaz moderna y fluida. ¿En qué puedo ayudarte hoy?' }
  ]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [isSettingsOpen, setIsSettingsOpen] = useState(false);
  const [activeTab, setActiveTab] = useState<'cuenta' | 'novedades'>('cuenta');
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(scrollToBottom, [messages]);

  const handleSend = async () => {
    if (!input.trim() || isLoading) return;

    const userMessage: Message = {
      id: Date.now().toString(),
      role: 'user',
      content: input,
    };

    setMessages(prev => [...prev, userMessage]);
    setInput('');
    setIsLoading(true);

    // Si el token no está configurado, usamos una respuesta simulada
    if (HF_API_KEY === "TU_TOKEN_AQUI") {
      setTimeout(() => {
        const assistantMessage: Message = {
          id: (Date.now() + 1).toString(),
          role: 'assistant',
          content: 'Esta es una respuesta de prueba. Para usar IA real, configura tu token de Hugging Face en el código.',
        };
        setMessages(prev => [...prev, assistantMessage]);
        setIsLoading(false);
      }, 1000);
      return;
    }

    const aiResponse = await queryHuggingFace(input);

    const assistantMessage: Message = {
      id: (Date.now() + 1).toString(),
      role: 'assistant',
      content: aiResponse,
    };
    setMessages(prev => [...prev, assistantMessage]);
    setIsLoading(false);
  };

  return (
    <div className="relative h-screen w-full bg-[#020202] overflow-hidden text-white selection:bg-blue-500/30 font-sans">
      {/* Background Animated Blobs */}
      <div className="absolute inset-0 overflow-hidden pointer-events-none">
        <motion.div
          animate={{
            scale: [1, 1.2, 1],
            rotate: [0, 90, 0],
          }}
          transition={{ duration: 25, repeat: Infinity, ease: "linear" }}
          className="absolute -top-[10%] -left-[10%] w-[70%] h-[70%] bg-[#000814] rounded-full blur-[120px] opacity-40"
        />
        <motion.div
          animate={{
            scale: [1, 1.1, 1],
            x: [0, -100, 0],
          }}
          transition={{ duration: 20, repeat: Infinity, ease: "linear" }}
          className="absolute top-[20%] -right-[10%] w-[60%] h-[60%] bg-[#01160a] rounded-full blur-[130px] opacity-30"
        />
        <motion.div
          animate={{
            scale: [1, 1.3, 1],
            y: [0, -50, 0],
          }}
          transition={{ duration: 30, repeat: Infinity, ease: "linear" }}
          className="absolute -bottom-[20%] left-[10%] w-[80%] h-[80%] bg-[#020205] rounded-full blur-[150px] opacity-60"
        />
      </div>

      {/* Main Content */}
      <div className="relative z-10 flex flex-col h-full max-w-4xl mx-auto px-4 py-4 md:py-8">
        {/* Header */}
        <header className="flex items-center justify-between mb-6 md:mb-10">
          <motion.div
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            className="flex items-center gap-3"
          >
            <div className="relative group">
              <div className="absolute -inset-1 bg-gradient-to-r from-blue-400 to-blue-600 rounded-xl blur opacity-25 group-hover:opacity-50 transition duration-1000"></div>
              <div className="relative w-12 h-12 rounded-xl overflow-hidden shadow-2xl shadow-blue-500/20 border border-white/10">
                <img src="/carl_logo.jpeg" alt="Carl Logo" className="w-full h-full object-cover" />
              </div>
            </div>
            <div>
              <h1 className="text-2xl md:text-3xl font-black tracking-tighter bg-clip-text text-transparent bg-gradient-to-r from-white via-white to-gray-500">
                Carl AI
              </h1>
              <p className="text-[10px] uppercase tracking-[0.2em] text-blue-500/80 font-bold">Premium Assistant</p>
            </div>
          </motion.div>

          <motion.button
            whileHover={{ scale: 1.05, backgroundColor: "rgba(255,255,255,0.12)" }}
            whileTap={{ scale: 0.95 }}
            onClick={() => setIsSettingsOpen(true)}
            className="p-3 rounded-2xl bg-white/5 border border-white/10 hover:bg-white/10 transition-all backdrop-blur-2xl group shadow-xl"
          >
            <Settings size={22} className="group-hover:rotate-90 transition-transform duration-500 text-gray-300" />
          </motion.button>
        </header>

        {/* Chat Area */}
        <div className="flex-1 overflow-y-auto mb-6 pr-2 space-y-6 custom-scrollbar">
          <AnimatePresence mode='popLayout'>
            {messages.map((msg) => (
              <motion.div
                key={msg.id}
                initial={{ opacity: 0, y: 15, scale: 0.98 }}
                animate={{ opacity: 1, y: 0, scale: 1 }}
                layout
                className={cn(
                  "flex items-start gap-3 md:gap-4 max-w-[90%] md:max-w-[85%]",
                  msg.role === 'user' ? "ml-auto flex-row-reverse" : "mr-auto"
                )}
              >
                <div className={cn(
                  "w-10 h-10 rounded-xl flex items-center justify-center flex-shrink-0 mt-1 shadow-lg backdrop-blur-md transition-transform duration-300 hover:scale-110 overflow-hidden border border-white/10",
                  msg.role === 'assistant'
                    ? "bg-forest-dark"
                    : "bg-deep-blue text-blue-400"
                )}>
                  {msg.role === 'assistant' ? (
                    <img src="/carl_logo.jpeg" alt="AI" className="w-full h-full object-cover" />
                  ) : (
                    <User size={18} />
                  )}
                </div>

                <div className={cn(
                  "px-5 py-4 rounded-3xl backdrop-blur-[40px] border transition-all duration-300",
                  msg.role === 'assistant'
                    ? "bg-white/5 border-white/10 rounded-tl-none text-gray-100 shadow-xl shadow-black/20"
                    : "bg-gradient-to-br from-blue-500/10 to-blue-600/5 border-blue-500/20 rounded-tr-none text-blue-50/90 shadow-xl shadow-blue-900/10"
                )}>
                  <p className="leading-relaxed text-[15px] md:text-base font-medium whitespace-pre-wrap">{msg.content}</p>
                </div>
              </motion.div>
            ))}
            {isLoading && (
              <motion.div
                initial={{ opacity: 0, scale: 0.8 }}
                animate={{ opacity: 1, scale: 1 }}
                className="flex items-center gap-3 mr-auto"
              >
                <div className="w-10 h-10 rounded-xl bg-forest-dark border border-white/10 flex items-center justify-center overflow-hidden">
                  <Loader2 className="animate-spin text-blue-400 absolute z-10" size={18} />
                  <img src="/carl_logo.jpeg" alt="AI" className="w-full h-full object-cover opacity-50" />
                </div>
                <div className="px-5 py-3 rounded-2xl bg-white/5 border border-white/10 backdrop-blur-xl">
                  <div className="flex gap-1">
                    <motion.span animate={{ opacity: [0.3, 1, 0.3] }} transition={{ repeat: Infinity, duration: 1 }} className="w-1.5 h-1.5 bg-blue-500 rounded-full" />
                    <motion.span animate={{ opacity: [0.3, 1, 0.3] }} transition={{ repeat: Infinity, duration: 1, delay: 0.2 }} className="w-1.5 h-1.5 bg-blue-500 rounded-full" />
                    <motion.span animate={{ opacity: [0.3, 1, 0.3] }} transition={{ repeat: Infinity, duration: 1, delay: 0.4 }} className="w-1.5 h-1.5 bg-blue-500 rounded-full" />
                  </div>
                </div>
              </motion.div>
            )}
          </AnimatePresence>
          <div ref={messagesEndRef} />
        </div>

        {/* Input Area */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="relative group mt-auto"
        >
          <div className="absolute -inset-1 bg-gradient-to-r from-blue-500/10 via-blue-500/10 to-blue-500/10 rounded-[2rem] blur-xl opacity-0 group-focus-within:opacity-100 transition duration-1000"></div>
          <div className="relative flex items-center gap-2 p-2.5 rounded-[1.8rem] bg-white/[0.03] border border-white/10 backdrop-blur-[50px] shadow-2xl transition-all duration-300 group-focus-within:border-white/20 group-focus-within:bg-white/[0.05]">
            <input
              type="text"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={(e) => e.key === 'Enter' && handleSend()}
              placeholder="Pregúntale a Carl algo asombroso..."
              disabled={isLoading}
              className="flex-1 bg-transparent border-none outline-none px-5 py-3 text-white placeholder:text-gray-500 md:text-lg"
            />
            <motion.button
              whileHover={{ scale: 1.05, boxShadow: "0 0 20px rgba(37, 99, 235, 0.4)" }}
              whileTap={{ scale: 0.95 }}
              onClick={handleSend}
              disabled={isLoading}
              className="p-4 rounded-2xl bg-blue-600 text-white shadow-lg shadow-blue-600/30 hover:bg-blue-500 transition-all disabled:opacity-50 disabled:cursor-not-allowed group"
            >
              <Send size={22} className="group-hover:translate-x-0.5 group-hover:-translate-y-0.5 transition-transform" />
            </motion.button>
          </div>
        </motion.div>

        <footer className="mt-4 text-center">
          <p className="text-[10px] text-gray-600 font-medium uppercase tracking-widest">Carley Interactive Studio 2026 todos derechos reservados</p>
        </footer>
      </div>

      {/* Settings Modal */}
      <AnimatePresence>
        {isSettingsOpen && (
          <div className="fixed inset-0 z-50 flex items-center justify-center p-4">
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
              onClick={() => setIsSettingsOpen(false)}
              className="absolute inset-0 bg-black/80 backdrop-blur-xl"
            />
            <motion.div
              initial={{ opacity: 0, scale: 0.9, y: 30 }}
              animate={{ opacity: 1, scale: 1, y: 0 }}
              exit={{ opacity: 0, scale: 0.9, y: 30 }}
              className="relative w-full max-w-2xl overflow-hidden rounded-[2.5rem] bg-[#0A0A0A] border border-white/10 shadow-2xl shadow-black/80"
            >
              <div className="flex flex-col md:flex-row h-[500px]">
                {/* Sidebar */}
                <div className="w-full md:w-2/5 border-b md:border-b-0 md:border-r border-white/10 bg-white/[0.02] p-6 flex flex-col gap-3">
                  <div className="mb-4">
                    <h2 className="text-xl font-bold px-2">Configuración</h2>
                  </div>
                  <button
                    onClick={() => setActiveTab('cuenta')}
                    className={cn(
                      "flex items-center gap-3 p-3.5 rounded-2xl transition-all duration-300",
                      activeTab === 'cuenta' ? "bg-white/10 text-white shadow-lg" : "text-gray-500 hover:text-gray-300 hover:bg-white/5"
                    )}
                  >
                    <User size={20} />
                    <span className="font-semibold">Mi Cuenta</span>
                  </button>
                  <button
                    onClick={() => setActiveTab('novedades')}
                    className={cn(
                      "flex items-center gap-3 p-3.5 rounded-2xl transition-all duration-300",
                      activeTab === 'novedades' ? "bg-white/10 text-white shadow-lg" : "text-gray-500 hover:text-gray-300 hover:bg-white/5"
                    )}
                  >
                    <Info size={20} />
                    <span className="font-semibold">Novedades</span>
                  </button>
                </div>

                {/* Content */}
                <div className="flex-1 p-8 overflow-y-auto">
                  {activeTab === 'cuenta' ? (
                    <div className="h-full flex flex-col items-center justify-center text-center max-w-xs mx-auto">
                      <div className="relative mb-6">
                        <div className="absolute -inset-4 bg-blue-500/10 rounded-full blur-2xl"></div>
                        <div className="relative w-20 h-20 rounded-3xl bg-white/5 flex items-center justify-center border border-white/10 shadow-2xl">
                          <Lock size={32} className="text-gray-400" />
                        </div>
                      </div>
                      <h3 className="text-2xl font-bold mb-3">Acceso Restringido</h3>
                      <p className="text-gray-400 text-sm leading-relaxed mb-8">La sincronización en la nube y el historial persistente estarán disponibles en la próxima gran actualización.</p>
                      <button
                        disabled
                        className="w-full py-4 rounded-2xl bg-white/5 border border-white/10 text-gray-500 cursor-not-allowed font-bold text-sm uppercase tracking-widest transition-all"
                      >
                        Próximamente
                      </button>
                    </div>
                  ) : (
                    <div className="space-y-6">
                      <h3 className="text-2xl font-bold mb-6">Últimas Novedades</h3>
                      <div className="group p-5 rounded-3xl bg-white/[0.03] border border-white/5 hover:border-white/10 transition-all duration-300">
                        <div className="flex items-center gap-3 mb-3">
                          <div className="px-2.5 py-1 rounded-lg bg-blue-500/10 text-blue-500 text-[10px] font-black uppercase tracking-tighter">New</div>
                          <span className="text-xs font-bold text-gray-500 uppercase tracking-widest">Marzo 2024</span>
                        </div>
                        <h4 className="text-lg font-bold mb-2">Interfaz Vision Engine v1</h4>
                        <p className="text-sm text-gray-400 leading-relaxed">Hemos implementado un motor de diseño basado en Glassmorphism con desenfoque de fondo en tiempo real para una experiencia inmersiva.</p>
                      </div>
                      <div className="group p-5 rounded-3xl bg-white/[0.01] border border-white/5 opacity-60">
                        <div className="flex items-center gap-3 mb-3 text-blue-500">
                          <MessageSquare size={18} />
                          <span className="text-xs font-bold uppercase tracking-widest">En Desarrollo</span>
                        </div>
                        <h4 className="text-lg font-bold mb-2">Conectividad HF Direct</h4>
                        <p className="text-sm text-gray-400 leading-relaxed">Pronto podrás vincular cualquier modelo de Hugging Face directamente desde esta interfaz.</p>
                      </div>
                    </div>
                  )}
                </div>
              </div>
            </motion.div>
          </div>
        )}
      </AnimatePresence>
    </div>
  );
}
