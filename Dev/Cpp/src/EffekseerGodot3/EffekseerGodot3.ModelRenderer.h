﻿#pragma once

//----------------------------------------------------------------------------------
// Include
//----------------------------------------------------------------------------------
#include "EffekseerRenderer.ModelRendererBase.h"
#include "EffekseerGodot3.RendererImplemented.h"

//-----------------------------------------------------------------------------------
//
//-----------------------------------------------------------------------------------
namespace EffekseerGodot3
{
//----------------------------------------------------------------------------------
//
//----------------------------------------------------------------------------------
typedef ::Effekseer::ModelRenderer::NodeParameter efkModelNodeParam;
typedef ::Effekseer::ModelRenderer::InstanceParameter efkModelInstanceParam;
typedef ::Effekseer::SIMD::Vec3f efkVector3D;

class ModelRenderer;
using ModelRendererRef = Effekseer::RefPtr<ModelRenderer>;

class ModelRenderer : public ::EffekseerRenderer::ModelRendererBase
{
private:
	RendererImplemented* m_renderer = nullptr;
	std::array<std::unique_ptr<Shader>, 6> m_lightweightShaders;
	std::array<std::unique_ptr<Shader>, 6> m_softparticleShaders;

	ModelRenderer(RendererImplemented* renderer);

public:
	virtual ~ModelRenderer();

	static ModelRendererRef Create(RendererImplemented* renderer);

public:
	void BeginRendering(const efkModelNodeParam& parameter, int32_t count, void* userData);

	virtual void Rendering(const efkModelNodeParam& parameter, const InstanceParameter& instanceParameter, void* userData) override;

	void EndRendering(const efkModelNodeParam& parameter, void* userData);
};
//----------------------------------------------------------------------------------
//
//----------------------------------------------------------------------------------
} // namespace EffekseerGodot3
//----------------------------------------------------------------------------------
//
//----------------------------------------------------------------------------------

