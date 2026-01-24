import Chatbot from '@/components/Chatbot';
function App() {

  return (
    <div className='flex flex-col min-h-full w-full max-w-3xl mx-auto px-4'>
      <header className='sticky top-0 shrink-0 z-20 bg-transparent'>
        <div className='flex flex-col h-full w-full gap-1 pt-4 pb-2'>
          <div className='font-urbanist text-sm tracking-[0.35em] text-main-text/70'>NEUSTA</div>
          <h1 className='font-urbanist text-[1.65rem] font-semibold'>J4RVIS Chatbot</h1>
        </div>
      </header>
      <Chatbot />
    </div>
  );
}

export default App;
