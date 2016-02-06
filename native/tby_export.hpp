class TheBountyRenderEngine {
public:
    TheBountyRenderEngine();
    static const char* bl_label;
    static const char* bl_idname;
    static const bool bl_use_preview;
    static const char* tag;

    void update(void* data, void* scene);
    void render(void* scene);
private:
};

