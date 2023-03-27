#ifdef BIND
#undef BIND
#endif

#define BIND(T) \
	if (inst->as<IfcSchema::T>()) { \
		try { \
			taxonomy::item* item = map_impl(inst->as<IfcSchema::T>()); \
			if (item != nullptr) { \
				item->instance = inst; \
				try { \
					if (inst->as<IfcSchema::IfcRepresentationItem>() && !inst->as<IfcSchema::IfcStyledItem>() && \
						/* @todo */ \
						(item->kind() == taxonomy::SHELL || item->kind() == taxonomy::COLLECTION || item->kind() == taxonomy::EXTRUSION) \
					) { \
						auto style = find_style(inst->as<IfcSchema::IfcRepresentationItem>()); \
						if (style) { \
							((taxonomy::geom_item*)item)->surface_style = (taxonomy::style*) map(style); \
						} \
					} \
				} catch (const std::exception& e) { \
					Logger::Message(Logger::LOG_ERROR, std::string(e.what()) + "\nFailed to convert:", inst); \
				} \
			} else {\
				Logger::Message(Logger::LOG_ERROR,"Failed to convert:", inst);\
			} \
			return item; \
		} catch (const std::exception& e) { \
			Logger::Message(Logger::LOG_ERROR, std::string(e.what()) + "\nFailed to convert:", inst); \
		} \
		return nullptr; \
	}

#include "mapping.i"